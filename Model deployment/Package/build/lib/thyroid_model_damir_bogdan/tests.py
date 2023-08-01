"""
Testing script using unittest
"""

import unittest
import pandas as pd
from load_pipeline import *  # This is how to import the pipeline, use load_pipeline() function after this

# Load the pipeline
pipe = load_pipeline()

# Read the data
df = pd.read_csv("raw.csv")

# Split the data
X = df.drop("Class", axis=1)
y = df["Class"]

# Test class for checking input features of the pipeline
class TestPipeInputFeatures(unittest.TestCase):

    def test_pipe_predict_columns(self):
        expected_columns = ['age', 'sex', 'on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_medication', 'sick',
                            'pregnant', 'thyroid_surgery', 'I131_treatment', 'query_hypothyroid', 'query_hyperthyroid',
                            'lithium', 'goitre', 'tumor', 'hypopituitary', 'psych', 'TSH_measured', 'TSH', 'T3_measured',
                            'T3', 'TT4_measured', 'TT4', 'T4U_measured', 'T4U', 'FTI_measured', 'FTI', 'TBG_measured',
                            'TBG', 'referral_source']

        # Check if X contains the expected columns
        self.assertSetEqual(set(X.columns), set(expected_columns), "DataFrame X does not contain the expected columns")

        print("Test passed successfully! All columns/features are present!")

# Test class for checking the output of the pipeline
class TestPipePredictOutput(unittest.TestCase):

    def test_pipe_predict(self):
        result_array = pipe.predict(X)  # Call your pipe.predict() function here

        # Ensure the result is a NumPy array
        self.assertIsInstance(result_array, np.ndarray, "Expected a NumPy array, but got {type(result_array)}")

        # Check data type of elements in the array
        self.assertTrue(np.issubdtype(result_array.dtype, np.int64), "Expected int64 data type for array elements")

        # Check each value in the array
        for value in result_array:
            self.assertGreaterEqual(value, 0, f"Predicted value {value} is less than 0")
            self.assertLessEqual(value, 3, f"Predicted value {value} is greater than 3")

        print("Test passed successfully! Predicted values as intended!")

if __name__ == '__main__':
    unittest.main()
