use ndarray::Array1;
use pyo3::prelude::*;

#[pyclass]
struct MinRatioCycleFinder {
    cached_circulations: Vec<Array1<f64>>,
}

#[pymethods]
impl MinRatioCycleFinder {
    #[new]
    fn new(circulations: Vec<Vec<f64>>) -> Self {
        Self {
            // Stored as circulations with values 1 and -1 for used edges
            cached_circulations: circulations.into_iter().map(Array1::<f64>::from).collect(),
        }
    }

    fn find_min_ratio_cycle(&self, gradients: Vec<f64>, lengths: Vec<f64>) -> (f64, Vec<f64>) {
        let gradients = Array1::<f64>::from(gradients);
        let lengths = Array1::<f64>::from(lengths);

        let mut min_ratio = f64::INFINITY;
        let mut min_ratio_cycle = Array1::<f64>::zeros(0);

        for circulation in &self.cached_circulations {
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
}

#[pymodule]
fn min_ratio(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MinRatioCycleFinder>()?;
    Ok(())
}
