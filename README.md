# Model
A library for [Anvil Applications](https://anvil.works) that provides model object
perisistence using the data tables service.

Using this library, you can write simple code for your model that looks like:

```
@model
class Person:
    attributes = ["name"]
```

You can then use that class to create new Person
instances, save them to a data table, fetch them back and update them with code as simple as:

```
from .model import Person

person = Person(name="Owen")
person.save()

person.name = "Owen Campbell"
person.save()
```

And you can do that in both client and server side code!

## Credits
The development of this library was funded by [Nanovare SAS](https://www.mojofertility.co)

## Installation
There are two methods to install this module within your own application:

### 1. As a Dependency

  * Create a clone of this application within your own Anvil account using this link:

    [<img src="https://anvil.works/img/forum/copy-app.png" height='40px'>](https://anvil.works/build#clone:2MVSGI6X5XLOHJNE=F2FBUNOHSQGADHUEEZ3EQTT5)
  
  * At anvil, open the app in which you'd like to include model persistence and, from its settings menu, click 'Dependencies',
    and select your new cloned app in the dropdown.

### 2. By Direct Inclusion

  * In your anvil application, create a new module in the client code section and name it 'model_base'
  * In your anvil application, create a new module in the server code section and name it 'persistence'
  * Copy the entire content of `client_code/base.py` from this repository into your 'model_base' module
  * Copy the entire content of `server_code/persistence.py` from this repository into your 'persistence' module
  * Create a data table named 'sequence' with two colums: 'id' (text) and 'next' (number)
  
## Usage

### Client module

  * Create a new client code module and name it 'model'
  * Write the code for your model objects within that new module.
  * Create a data table for each model. Its name should be the same as the model's class name, but all lower case.
  * Create columns for each of the model's attributes and relationships (plus one called 'id' which must be a number column).

#### Models
  
  Each model object should:

  * be decorated with the '@model' decorator
  * include at least one name in its 'attributes' list
  * optionally, include entries in its 'relationships' list, each of which must be an instance of the 'Relationship' class

  For example, if we wanted to model employees of a company who each have a name and date on which they started work, we might write the following:

  ```
  from .base_model import model

  @model
  class Employee:
      attributes = ["name", "start_date"]
  ```

  and then create a data table with 'id', 'name' and 'start_date' columns. (The id column must be a number)

  If we wanted to create another class for departments within the organsiation and tag each employee to a department, we would:

  * Create the Department model class:
  * Create a data table for this new model with colums 'id' and 'name'
  * Add a relationship to our Person class

  The resulting model code would be:

  ```
  from .base_model import model, Relationship

  @model
  class Department:
      attributes = ["name"]


  @model
  class Employee:
      attributes = ["name", "start_date"]
      relationships = [Relationship(name="department", cls=Department)]
  ```

  Each of our classes now has several methods for interacting with our data tables:

  * .get - will fetch an instance of our model class from the database
  * .save - will create a new data tables row or update an exisiting row with new details
  * .list - will return a SearchIterator of data tables rows

  For example, to create a new department and an employee within that department, we might write:

  ```
  import datetime as dt
  from .model import Employee, Department

  department = Department(name="IT")
  department.save()

  employee = Employee(name="Owen", start_date=dt.datetime(2015, 3, 22), department=department)
  employee.save()
  ```

  Elsewhere, we might want to fetch the employee object from the database:

  ```
  from .model import Employee

  employee = Employee.get(id=1)
  ```
  