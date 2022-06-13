# python module name should be all lowercase, short named with eventual underscore if it increases readability
# note there is a space after the #
# this is all following PEP-8 Style Guide
import os
from datetime import datetime, timedelta
from io import StringIO
from typing import Final  # used for constant variables
import configparser

import boto3
import pandas as pd
import warnings
import response

from memory_profiler import profile


warnings.filterwarnings("ignore")  # ignoring warnings for future deprecated methods
os.environ["PYTHONWARNINGS"] = "ignore"  # affects subprocesses
module_compression = ""


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    print("sections :" + str(config.sections()))
    compression = str(config['DEFAULT']['Compression'])
    print("first compression: " + compression)
    module_compression = compression


@profile()
def first_proc() -> None:
    # lowercase, with words separated by underscores as necessary to improve readability
    __a = 10  # a private variable

    print("two lines between procedures, functions, classes and its properties")
    datetime_obj = datetime.strptime("1/1/2022", "%d/%m/%Y")
    print(
        f"SomeClass class variable f{SomeClass.class_var}"
    )  # you can access class variables
    a = SomeClass("a", datetime_obj, 0)
    xx = a.days_ago()
    print(f"xx {xx}")
    drugi = SomeClass("drugi", datetime_obj, 10)
    treci = SomeClass("drugi", datetime_obj, 20)
    cet = SomeClass("drugi", datetime_obj, 30)
    c = __a * 2


@profile()  # annotation that marks code that will be profiled for memory usage
def test():
    dict1 = {"name": "a", "id": 0}
    dff = pd.DataFrame(dict1, index=[1])

    for x in range(1, 10000):
        dict2 = {"name": "a", "id": x}
        dff = dff.append(dict2, ignore_index=True)
    print("kraj ucitavanja")


class SomeClass:
    NUMBER_OF_DAYS: Final[int] = 30  # the only way how to indicate the variable should be considered constant
    class_var = "SomeClass name"  # class level variable

    def __str__(self):
        retval = ("SomeClass:    class_var: " + self.class_var + ", fdate: " + str(self.fdate))
        return retval

    # class name should follow Camel Case notation
    def __init__(
        self, some: str, fdate: datetime, quantity: int = 0
    ):  # these are only annotations
        # assert used only in testing
        assert (len(some) > 0), "param some should not be empty"  # validation that can be used in constructor
        assert (fdate is not None), "fdate param cannot be None"  # we check if param doesn't satisfy validation criteria
        assert (type(fdate) is datetime), "fdate is not datetime"  # we can do some type checking
        assert (fdate - timedelta(30) < datetime.now()), "date cannot be more than 30 days ago"  # some business logic
        self.fdate = fdate
        self.quantity = quantity
        self.some = some

    def _internal_calc(
        self,
    ) -> None:  # methods with single leading underscore marks internal method (can be visible outside)
        pass

    def add_elements(self, *element) -> None:
        pass

    def days_ago(self) -> int:  # tells what is a return type
        retval = (datetime.now() - self.fdate).days
        print(f"days retval {retval}")
        return retval


if __name__ == "__main__":
    # first_proc()
    load_config()
    print("opet compression: " + module_compression)
    datum = datetime.strptime("10/10/2020", "%d/%m/%Y")
    krivi = "10.10.2020"
    a = SomeClass("some text", datum, 10)
    print(a)
    # bb = [0, 1, None, 2]
    # print("b: " + bb)

    test()

    def test2():
        r = response.Response("module_name", "")
        print("response: " + str(r.if_all_params_exist(0, 1, None, 2)))

        s3 = boto3.resource("s3")
        bucket = s3.Bucket("deutsche-boerse-xetra-pds")

        bucket_obj = bucket.objects.filter(Prefix="2021-03-15")
        objects = [obj for obj in bucket_obj]

        csv_obj_init = (
            bucket.Object(key=objects[0].key).get().get("Body").read().decode("utf-8")
        )
        data = StringIO(csv_obj_init)
        df_init = pd.read_csv(data, delimiter=",")

        df_all = pd.DataFrame(columns=df_init.columns)
        for obj in objects:
            csv_obj = (
                bucket.Object(key=obj.key).get().get("Body").read().decode("utf-8")
            )
            data = StringIO(csv_obj)
            df = pd.read_csv(data, delimiter=",")
            df_all.append(df, ignore_index=True)
            df_all = df_all.append(df, ignore_index=True)
