# DEND-Capstone-Project

Build an Data Lake using Spark And Copy Data from S3 bucket,then process data and store datat ables into S3 bucket.


### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Run](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

[Installing Python, JDK, Spark](https://sundog-education.com/spark-python)


## Project Motivation<a name="motivation"></a>
A music streaming startup, Sparkify, has grown their user base and song database and want to move their data warehouse to a data lake. Their data resides in S3, in a directroy of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app
### Fact table and Dimension table with star schemas
![Star Schemas](./assets/star_schemas.jpg)


## File Descriptions <a name="files"></a>

```
- LICENSE
- README.md
- data   # raw data files
- image # project relevant images
- docker-airflow #  DAG files 
- research.ipynb # The project jupyter notebook file
```

## Run <a name="results"></a>

```
spark-submit etl.py

```

## Licensing, Authors, and Acknowledgements <a name="licensing"></a>

### Built With
* [spark sql](https://spark.apache.org/docs/latest/) - Pyspark API
* [Million Song Dataset](http://millionsongdataset.com/)
* [Event simulator](https://github.com/Interana/eventsim)

### Versioning

* We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

### Authors

* **Tom Ge** - *Data egineer* - [github profile](https://github.com/tomgtqq)

### License

* This project is licensed under the MIT License

