import re
import unittest
import read_files

class Test_row(unittest.TestCase):
    ''' Class to test the row object used to read the csv file'''
    
    def test_row(self):
        # test one class for credit and one for debit
        name = ['row1', 'row2']
        date = ['12/05/2022', '15/05/2022']
        description = ['Salary', 'Other']
        credit = [2000, 0]
        debit = [0, -430]
        balance =[ 500, 500]

        for i in range(2):
            obj = read_files.Row(name[i], date[i], description[i], credit[i], debit[i], balance[i])

            # Assert if credit
            if credit[i] > 0 and debit[i] == 0:
                self.assertTrue(obj.is_credit())
                self.assertFalse(obj.is_debit())

            # Assert if debit
            elif credit[i] == 0 and debit[i] < 0:
                self.assertTrue(obj.is_debit())
                self.assertFalse(obj.is_credit())

            # Tests getters
            self.assertEqual(obj.get_name(), name[i])
            self.assertEqual(obj.get_balance(), balance[i])
            self.assertEqual(obj.get_credit(), credit[i])
            self.assertEqual(obj.get_debit(), debit[i])
            self.assertEqual(obj.get_date(), date[i])
            self.assertEqual(obj.get_description(), description[i])


if __name__ == '__main__':
    unittest.main()

# class Test_read_csv(unittest.TestCase):

# class Test_format_Date(unittest.TestCase):

# Tests for read_files.py
