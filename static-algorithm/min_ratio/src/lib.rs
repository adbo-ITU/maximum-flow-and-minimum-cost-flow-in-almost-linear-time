use ndarray::Array1;
use pyo3::prelude::*;
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};

#[pyclass]
struct MinRatioCycleFinder {
    cached_circulations: Vec<Array1<f64>>,
    chunks: Vec<Vec<Array1<f64>>>,
}

const CHUNK_SIZE: usize = 50_000;

#[pymethods]
impl MinRatioCycleFinder {
    #[new]
    fn new(circulations: Vec<Vec<f64>>) -> Self {
        // Stored as circulations with values 1 and -1 for used edges
        let cached_circulations = circulations
            .into_iter()
            .map(Array1::<f64>::from)
            .collect::<Vec<_>>();

        let chunks = cached_circulations
            .chunks(CHUNK_SIZE)
            .map(|chunk| chunk.to_vec())
            .collect();

        Self {
            cached_circulations,
            chunks,
        }
    }

    fn find_min_ratio_cycle(&self, gradients: Vec<f64>, lengths: Vec<f64>) -> (f64, Vec<f64>) {
        let gradients = Array1::<f64>::from(gradients);
        let lengths = Array1::<f64>::from(lengths);

        let (min_ratio, min_ratio_cycle) = if self.cached_circulations.len() < CHUNK_SIZE {
            find_min_ratio_cycle(&self.cached_circulations, &gradients, &lengths)
        } else {
            self.chunks
                .par_iter()
                .map(|chunk| find_min_ratio_cycle(chunk, &gradients, &lengths))
                .reduce(
                    || (f64::INFINITY, Array1::<f64>::zeros(0)),
                    |(min_ratio, min_ratio_cycle), (fold_ratio, fold_cycle)| {
                        if fold_ratio < min_ratio {
                            (fold_ratio, fold_cycle)
                        } else {
                            (min_ratio, min_ratio_cycle)
                        }
                    },
                )
        };

        (min_ratio, min_ratio_cycle.to_vec())
    }
}

fn find_min_ratio_cycle(
    circulations: &[Array1<f64>],
    gradients: &Array1<f64>,
    lengths: &Array1<f64>,
) -> (f64, Array1<f64>) {
    let mut min_ratio = f64::INFINITY;
    let mut min_ratio_cycle = Array1::<f64>::zeros(0);

    for circulation in circulations {
        for dir in [1.0, -1.0].into_iter() {
            let delta = circulation * dir;

            let gd = gradients.dot(&delta);
            let lxd = lengths * delta;
            let norm = lxd.abs().sum();
            let ratio = gd / norm;

            if ratio < min_ratio {
                min_ratio = ratio;
                min_ratio_cycle = circulation.clone();
            }
        }
    }

    (min_ratio, min_ratio_cycle)
}

#[pymodule]
fn min_ratio(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MinRatioCycleFinder>()?;
    Ok(())
}
