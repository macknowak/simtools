Changelog
=========

0.1.0 - Unreleased
------------------

### Added

- Added container storing parameters (class `simtools.Params`). It is a type of
  a dictionary that provides access to values both through keys and through
  attributes, and also provides the following functionality: loading parameters
  from a file (which supports JSON files and Python files) and saving
  parameters to a file (which supports JSON files).
- Added loading parameters from a file (function `simtools.load_params()`). It
  is a convenient function that creates an object of class `simtools.Params`
  and populates it with parameters loaded from a file.
- Added container storing parameter sets (class `simtools.ParamSets`). It is a
  type of a mutable sequence, whose elements are objects of class
  `simtools.Params`, that also provides the following functionality: loading
  parameters from a file as a parameter set (which supports JSON files and
  Python files) and saving all parameter sets to a file (which supports CSV
  files and JSON files).
- Added saving software versions to a JSON file (function
  `simtools.save_versions()`). It is a function that saves to a file
  information on software versions, which include software name and version
  number.
- Added saving platform information to a JSON file (function
  `simtools.save_platform()`). It is a function that saves to a file the
  following information: computer's network name, machine type, processor name,
  operating system name, system's release, and system's release version.
- Added parsing command line arguments (functions `simtools.parse_args()` and
  `simtools.parse_known_args()`). These are functions that recognize command
  line arguments that are defined in SimTools as model built-in options or are
  specified as model custom options.
- Added generating simulation id based on local date and time (function
  `simtools.generate_sim_id()`). It is a function that generates a simulation
  id that combines information on the current year, month, day of the month,
  hour, minute, and second at the moment of execution.
- Added generating simulation directory name (function
  `simtools.generate_sim_dirname()`). It is a function that generates a
  simulation directory name that is based on a simulation id.
- Added creating directory structure for simulation (function
  `simtools.make_dirs()`). It is a function that creates a directory structure
  that comprises an optional simulation master directory, a simulation
  directory, and an optional data directory.
- Added launching simulation (function `simtools.run_sim()`). It is a function
  that launches a simulation of a model as a child process, passing all
  relevant command line arguments to the model.
- Added normalizing the format of executable (function
  `simtools.norm_executable()`). It is a function that splits the executable
  name from possible arguments and, if the executable is specified as a
  relative path, determines the corresponding absolute path.
- Added exporting parameters of multiple simulations to a file (function
  `simtools.export_params()`). It is a function that loads parameters of each
  of the specified simulations from the corresponding parameter file as a
  parameter set and then saves all the parameter sets to a file.
- Added loading parameter names from a text file (function
  `simtools.load_paramnames()`). It is a function that loads parameter names
  from a file that contains one parameter name (optionally with a substitute
  name) per line.
- Added loading names of simulation directories from a text file (function
  `simtools.load_sim_dirnames()`). It is a function that loads names of
  simulation directories from a file that contains one directory name (or
  directory path) per line.
- Added generating random seed using OS-specific randomness source (function
  `simtools.generate_seed()`). It is a function that produces highly
  unpredictable random bytes (theoretically so unpredictable that they could be
  used even in cryptographic applications).
- Added simulation launcher console script (file `bin/runsim.py`). It is a
  script that launches a model simulation in a designated directory in the
  following manner: it first creates an appropriate directory structure
  including a simulation directory, generating a simulation id if necessary,
  then changes the current working directory to the simulation directory, and
  finally launches a simulation as a child process, passing all relevant
  command line arguments to the model.
- Added parameter exporter console script (file `bin/exppar.py`). It is a
  script that exports parameters of multiple simulations to a file in the
  following manner: it first loads from a text file the names of parameters to
  be exported along with an optional mapping that defines how these names
  should be substituted with different ones, then loads from another text file
  the names of relevant simulation directories, and finally, as the parameters
  are collected by traversing the simulation directories and loading
  appropriate parameter files, it exports them to a file.
- Added random seed generator console script (file `bin/genseed.py`). It is a
  script that generates a random seed using OS-specific randomness source and
  then prints it.
- Added hierarchy of SimTools exceptions: the base SimTools exception (class
  `simtools.exceptions.SimToolsError`) and an exception related to an error
  during processing a file (class `simtools.exceptions.FileError`).
- Added the base SimTools warning (class
  `simtools.exceptions.SimToolsWarning`).

### Documentation

- Added package description (file `README.md`). It includes a general
  characteristic of the package and an example that demonstrates how basic
  package features can be utilized.
- Added package license terms (file `LICENSE.txt`). The package is licensed
  according to the terms and conditions of the GNU General Public License,
  version 3.
- Added an example model demonstrating basic package features (directory
  `examples/basic`). It is a model that concerns a vertical spring-mass system
  in a gravitational field, which is subject to damping, and demonstrates the
  following features: separation of the actual model from its parameters; use
  of basic options (`params_filename`, `save_data`, `sim_id`); loading
  parameters from the parameter file; employment of a simulation id; saving
  data generated by the model during a simulation; saving parameters; saving
  metadata (platform information and software versions).
- Added an example model demonstrating use of various options (directory
  `examples/options`). It is a model that concerns a vertical spring-mass
  system in a gravitational field, which is subject to damping, and
  demonstrates the following features: separation of the actual model from its
  parameters; use of various options (`data_dirname`, `params_filename`,
  `save_data`, `sim_id`, and a custom option `verbose`); loading parameters
  from the parameter file; employment of a simulation id; saving data generated
  by the model during a simulation; saving parameters; saving metadata
  (platform information and software versions).
