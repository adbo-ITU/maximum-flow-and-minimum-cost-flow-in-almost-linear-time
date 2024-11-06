use ndarray::Array1;
use pyo3::prelude::*;

#[pyfunction]
fn find_min_ratio_cycle(
    edge_cycles: Vec<Vec<f64>>,
    gradients: Vec<f64>,
    lengths: Vec<f64>,
) -> (f64, Vec<f64>) {
    let gradients = Array1::<f64>::from(gradients);
    let lengths = Array1::<f64>::from(lengths);

    // Stored as circulations with values 1 and -1 for used edges
    let cycles = edge_cycles
        .into_iter()
        .map(Array1::<f64>::from)
        .collect::<Vec<_>>();

    let mut min_ratio = f64::INFINITY;
    let mut min_ratio_cycle = Array1::<f64>::zeros(0);

    for circulation in cycles.iter() {
        for dir in [1.0, -1.0].into_iter() {
            let delta = circulation * dir;

            let gd = gradients.dot(&delta);
            let lxd = &lengths * &delta;
            let norm = lxd.abs().sum();
            let ratio = gd / norm;

            if ratio < min_ratio {
                min_ratio = ratio;
                min_ratio_cycle = circulation.clone();
            }
        }
    }

    (min_ratio, min_ratio_cycle.to_vec())
}

#[pymodule]
fn min_ratio(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_min_ratio_cycle, m)?)?;
    Ok(())
}
