//
// COPYRIGHT C 1999- Ali Dasdan (ali_dasdan@yahoo.com)
//
//
// An implementation of Howard's minimum cycle ratio algorithm. This
// implementation is quite a bit different from the original
// implementation given by Gaubert et al.
//

// Parameters of interest: NITER, NCYCLES, CYCLELEN, CHECK_LIMIT,
// NUPDATES, QUEUELEN, NEDGES, not_improved.

// count[0] = number of iterations to finish
// count[1] = number of iterations to find final lambda

#include "ad_graph.h"
#include "ad_queue.h"

// More node info for Howard's algorithm. For a node u,
// more_ninfo[u].policy = (u, more_ninfo[u].target). Carrying target,
// einfo (weight of policy edge), and einfo2 (transit time of policy
// edge) is redundant but it makes running time faster by eliminating
// access to the edge list.
struct ninfo_how {
    float dist;    // node potential.
    int   visited; // set if node is visited for some purpose.
    int   policy;  // successor edge.
    int   target;  // successor node
    int   einfo;   // weight of policy edge.
    int   einfo2;  // transit time of policy edge.
};

float
find_min_cycle_ratio_for_scc( const ad_graph< ninfo > *g, 
                              int plus_infinity,
                              float lambda_so_far )
{
    int n = g->num_nodes();
    int m = g->num_edges();

    ninfo_how        *more_ninfo = new ninfo_how[ n ];
    ad_queue< int >  nodeq( n );

    float f_plus_infinity = ( float ) plus_infinity;

    // STEP: Find the initial policy graph:
    for ( int v = 0; v < n; ++v )
        more_ninfo[ v ].dist = f_plus_infinity;

    for ( int e = 0; e < m; ++e ) {
        int u = g->source( e );
        int d = g->edge_info( e );

        if ( d < more_ninfo[ u ].dist ) {
            more_ninfo[ u ].dist = ( float ) d;
            more_ninfo[ u ].policy = e;
            more_ninfo[ u ].target = g->target( e );
            more_ninfo[ u ].einfo = d;
            more_ninfo[ u ].einfo2 = g->edge_info2( e );
        }
    }

    float lambda = lambda_so_far;

    int CHECK_LIMIT = n;
    int CHECK_COUNT = 0;

    while ( true ) {
        // STEP: Find the min mean cycle in the policy graph. Note that
        // each connected component in the policy graph has exactly one
        // cycle.
        for ( int v = 0; v < n; ++v )
            more_ninfo[ v ].visited = -1;

        int best_node = -1;  // A node in the cycle with the smallest mean.
                             //
        // At the exit of this loop, visited field of every node must be >
        // nonnegatice (-1 to be exact).
        for ( int v = 0; v < n; ++v ) {

            if ( 0 <= more_ninfo[ v ].visited )
                continue;

            // Search for a new cycle:
            int u = v;
            do {
                more_ninfo[ u ].visited = v;
                u = more_ninfo[ u ].target;
            } while ( -1 == more_ninfo[ u ].visited );

            if ( v != more_ninfo[ u ].visited )
                continue;

            // Compute the mean of the cycle found. Note that u is a node on
            // this cycle.
            int w = u;
            int total_weight = 0;
            int total_length = 0;
            do {
                ++total_length;
                total_weight += more_ninfo[ u ].einfo;
                u = more_ninfo[ u ].target;
            } while ( u != w );

            // Update lambda only if it decreases.
            float new_lambda = ( float ) total_weight / total_length;
            if ( new_lambda < lambda ) {
                lambda = new_lambda;
                best_node = u;
            }
        } // for v

        if ( -1 == best_node ) {
            // '-1 == best_node' implies that lambda has not changed. Then,
            // if there is no change for CHECK_LIMIT times, we decide that
            // the algorithm converges and we exit.

            if ( CHECK_COUNT++ > CHECK_LIMIT ) {
                break;
            }

        } else {
            // '-1 != best_node' implies that lambda has changed.
            CHECK_COUNT = 0;

            // STEP: Update the dist of every predecessor node of best_node
            // using a reverse breadth-first search ( BFS ):

            nodeq.init();
            nodeq.put( best_node );

            // visited is greater than -1 for every node at this point. We
            // can use this fact as follows. Below we only need a
            // (visited/not visited) for visited. Thus, we designate that -1
            // means "visited", and any other value means "not
            // visited". Initially, every node is not visited.
            more_ninfo[ best_node ].visited = -1;

            while ( nodeq.is_not_empty() ) {
                int v = nodeq.get();

                for ( int i = 0; i < g->indegree( v ); ++i ) {
                    int u = g->ith_source_node( v, i );

                    if ( -1 != more_ninfo[ u ].visited ) {
                        if ( v == more_ninfo[ u ].target ) {
                            more_ninfo[ u ].visited = -1;
                            more_ninfo[ u ].dist = more_ninfo[ v ].dist + 
                                more_ninfo[ u ].einfo - lambda * more_ninfo[ u ].einfo2;
                            nodeq.put( u );
                        }
                    }
                }
            } // while nodeq 
        }  // if best_node != -1

        // STEP: Update the dist of the other nodes:
        bool not_improved = true;

        for ( int e = 0; e < m; ++e ) {
            int u = g->source( e );
            int v = g->target( e );

            float new_dist = more_ninfo[ v ].dist + 
                g->edge_info( e ) - lambda * g->edge_info2( e );

            if ( EPSILON < ( more_ninfo[ u ].dist - new_dist ) ) {
                not_improved = false;
                more_ninfo[ u ].dist = new_dist;
                more_ninfo[ u ].policy = e;
                more_ninfo[ u ].target = v;
                more_ninfo[ u ].einfo = g->edge_info( e );
                more_ninfo[ u ].einfo2 = g->edge_info2( e );
            }
        }

        if ( not_improved ) {
            break;
        } 
    }  // main while loop

    delete [] more_ninfo;

    return lambda;
}  // find_min_cycle_ratio_for_scc
