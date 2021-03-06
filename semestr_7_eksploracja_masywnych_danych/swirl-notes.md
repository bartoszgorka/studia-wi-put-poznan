## Swirl Notes
* No instant calculations - if can ignore it, just ignore and calculate when really need value
* `<-` is a assignment operator
* Even a single numeric value is a `vector` of length one - as result we have `[1] value`
* Vectors can be generated with function `c(elem1, elem2 ...)`
* If we need help, we can use `?function` to show `R documentation`
* Operators `+`, `-`, `/`, and `^` (square)
* When vectors are the same length, R can performs the specified arithmetic element-by-element. When we have for example `(vector of length 4) * 2` we have `vector * c(2, 2, 2, 2)`. `c(1, 2, 3, 4) + c(0, 10)` as result generate `1 12 3 14`
* By `data$field` - operator `$` we can grab specific items from `data`
* Sequences can be generated by `start value : end value` (without spaces). When `start < end` we will receive counted backwards. As step we always have `1`. To use custom step we should call `seq()`
* Build-in functions are highly optimized - in our code we should use it
* `Atomic vector` contains exactly one data type, in `list` we can contain multiple data types
* `Logical vectors` can store `TRUE`, `FALSE` and `NA` values
* `LETTERS` - built-in vector with all 26 letters in the English alphabet
* Calculate how many `NA` values - `sum(is.na(vect))` - logical `TRUE` is equal to `1`
* `NaN` is `not a number` (part of `NA`)
* `x[1:10]` - get subset from vector `x` (indexes `1 .. 10`)
* In `R language` first element has index `1`!
* Get elements from vector except the 2nd and 10th element - `vector[c(-2, -10)]` (negative indexes will be ignored)
* Vectors can be named - `c(key1 = value1, key2 = value2 ...)`
* Names can be assign to already existing vector by `names(vect) <- c(name1, name2 ...)`
* `Matrix` can contain only a single class of data, `data frames` can consist of many different.
* `Vector` doesn't have a `dim` attribute
* Boolean value - `TRUE`, `FALSE`
* `NOT` can be generated by `!`
* With `&` we can compare boolean with each element of vector, with `&&` ONLY FIRST element will be check
* LAST ROW in function will be your's response
* Default parameter in function - `function(x, y = value) { ... }`
* Function can use function - `function(fun, data) { fun(data) }`
* Anonymous function - `f(function(x){ x + 1 }, 6)`
* `...` can be used in code just as `...` - for example `fun(...) { paste(...) }`. After `...` we MUST use named parameters
* Take args from `...` - `args <- list(...)`, next we can use names `args[['name']]`
* Binary operator `"%name$" <- function(left, right) { ... }` - always two args, name inside `"% %"`
* Dates can by represented by the `POSIXct` and `POSIXlt` classes, internally dates and times are stored as number of seconds since `1970-01-01`
* On dates, times we can perform operations (also arithmetic)
* `plot()`, `boxplot()` is easy graph creator in R language
* Formula `x ~ y` (for example in `plot()`) can be used to plot relationship between this variables

## Functions
* `sqrt()`
* `getwd()` - get current working directory
* `setwd(dir)` - can change current working directory
* `ls()` - list object, shows what data sets and functions a user has defined, we can check local variables
* `list.files()` or `dir()` - list all the files in working directory
* `args(function without parentheses)` - check arguments used by function
* `dir.create(dir name)` - create new directory
* `file.create(file name)` - create new regular file
* `file.exists(file name)` - check file exists
* `file.info(file name)` - file metadata
* `file.path` - construct file and directory paths, independent of the operating system
* `seq()` - create sequence
* `seq_along(vect)` - make sequence with length like `vect`, the same we will achieve when call `1:length(vect)` or `seq(along.with = vect)`
* `rep(value, times = X)` - replicate `value` `X` times, as `value` can use also a `vector`
* `paste(data, collapse = " ")` - join elements of vector into single text, can join two vectors always element-by-element
* `rnorm()` - standard normal distribution
* `sample()` - take a sample from data source
* `names(vect)` - get the names of `vect`
* `dim` - dimension, can be use to get or set by `dim(val) <- c(rows, cols)`
* `matrix(data, nrows = x, ncols = y)`
* `cbind` - combine columns - can force cast to `character` (coerce), to prevent it we should use `data.frame` instead of `matrix` data type
* `colnames` - columns with names from vector
* `which(vector OPT value)` - returns the indices of the vector that are `TRUE`
* `any()` and `all()`
* `head(data)` - take first 6 lines of data
* `lapply(data, function)` - takes a list as input, applies a functioon to each element of the list, then returns a list of the same length as the original one
* `sapply` will do similar work like `lapply`, also will simplify result
* `range(data)` - returns the minimum and maximum of data
* `vapply` allows us to specify correct format explicitly, when format doesn't match we will receive error
* `table(value)` - show `value` in tabular form
* `object.size(data)` - check how much space is occupying in memory by dataset
* `summary()` - dataset description for each variable, distribution
* `str()` -  structure of data
* `rbinom()`, `rnorm()`, `rpois()`
* `replicate()` - create a matrix with results of calculations
* `colMeans()` we can use to calculate mean of each column
* `hist()` can be used to show the distribution as a histogram (plot)
* `weekdays()`, `months()`, `quarters()`
* `strptime()` converts character vector to POSIXlt
