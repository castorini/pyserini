import os
import unittest
import tempfile
from pyserini.query_iterator import MBEIRQueryIterator, DefaultQueryIterator, KiltQueryIterator, MultimodalQueryIterator

class TestQueryIterators(unittest.TestCase):
    def test_mbeir_query_iterator(self):
        test_topics = {
            "text_only": {
                "qid": "text_only",
                "query_txt": "This is a text-only query",
                "query_img_path": None,
                "query_modality": "text",
                "instr_file": "sample_instructions.txt"
            },
            "null_string": {
                "qid": "null_string",
                "query_txt": "Query with null string path",
                "query_img_path": "null",
                "query_modality": "text",
                "instr_file": "sample_instructions.txt"
            },
            "valid_image": {
                "qid": "multimodal",
                "query_txt": "Query with image",
                "query_img_path": "images/test.jpg",
                "query_modality": "image,text",
                "instr_file": "sample_instructions.txt"
            },
            "empty_string": {
                "qid": "empty",
                "query_txt": "Query with empty path",
                "query_img_path": "",
                "query_modality": "text",
                "instr_file": "sample_instructions.txt"
            },
            "missing_field": {
                "qid": "missing_field",
                "query_txt": "Query with missing image path field",
                "query_modality": "text",
                "instr_file": "sample_instructions.txt"
            },
            "invalid_image": {  
                "qid": "invalid_img",
                "query_txt": "Query with invalid image path",
                "query_img_path": "images/invalid.jpg",
                "query_modality": "image,text",
                "instr_file": "sample_instructions.txt"
            },
            "empty_text_string": {
                "qid": "image_only",
                "query_txt": "",
                "query_img_path": "images/only_image.jpg",
                "query_modality": "image",
                "instr_file": "sample_instructions.txt"
            },
            "missing_text_field": {
                "qid": "missing_text",
                "query_img_path": "images/only_image2.jpg",
                "query_modality": "image",
                "instr_file": "sample_instructions.txt"
            }
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            images_dir = os.path.join(temp_dir, "images")
            os.makedirs(images_dir)
            with open(os.path.join(images_dir, "test.jpg"), 'w') as f:
                f.write("dummy image content")
            with open(os.path.join(images_dir, "only_image.jpg"), 'w') as f:
                f.write("dummy image content")
            with open(os.path.join(images_dir, "only_image2.jpg"), 'w') as f:
                f.write("dummy image content")

            iterator = MBEIRQueryIterator(test_topics, topic_dir=temp_dir)
            
            result = iterator.get_query("text_only")
            self.assertIsNone(result['query_img_path'])
            self.assertEqual(result['query_modality'], 'text')
            
            result = iterator.get_query("null_string")
            self.assertIsNone(result['query_img_path'])
            self.assertEqual(result['query_modality'], 'text')
            
            result = iterator.get_query("empty_string")
            self.assertIsNone(result['query_img_path'])
            self.assertEqual(result['query_modality'], 'text')
            
            result = iterator.get_query("valid_image")
            expected_path2 = os.path.join(temp_dir, "images/test.jpg")
            self.assertEqual(result['query_img_path'], expected_path2)
            self.assertEqual(result['query_modality'], 'image,text')

            result = iterator.get_query("missing_field")
            self.assertIsNone(result['query_img_path'])
            self.assertEqual(result['query_modality'], 'text')

            with self.assertRaises(FileNotFoundError):
                iterator.get_query("invalid_img")

            result = iterator.get_query("empty_text_string")
            self.assertEqual(result['query_txt'], '')
            self.assertEqual(result['query_modality'], 'image')

            result = iterator.get_query("missing_text_field")
            self.assertEqual(result['query_txt'], '')
            self.assertEqual(result['query_modality'], 'image')

    def test_default_query_iterator(self):
        topics = {
            "1": {"title": "first query"},
            "2": {"title": "second query"}
        }
        iterator = DefaultQueryIterator(topics)
        
        self.assertEqual(iterator.get_query("1"), "first query")
        self.assertEqual(iterator.get_query("2"), "second query")
        
        queries = list(iterator)
        self.assertEqual(len(queries), 2)
        self.assertEqual(queries[0], ("1", "first query"))

    def test_kilt_query_iterator(self):
        topics = {
            "test_id": {
                "id": "test_id",
                "input": "Sample [START_ENT]test[END_ENT] input"
            }
        }
        iterator = KiltQueryIterator(topics)
        
        result = iterator.get_query("test_id")  
        self.assertEqual(result, "Sample test input")
        self.assertNotIn("[START_ENT]", result)
        self.assertNotIn("[END_ENT]", result)

    def test_multimodal_query_iterator(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "test_query.txt")
            with open(test_file, 'w') as f:
                f.write("test query content")
            
            topics = {
                "1": {"path": "test_query.txt"}
            }
            
            MultimodalQueryIterator.topic_dir = temp_dir
            iterator = MultimodalQueryIterator(topics)
            
            result = iterator.get_query("1")
            self.assertEqual(result, test_file)
            
            topics["2"] = {"path": "missing.txt"}
            with self.assertRaises(FileNotFoundError):
                iterator.get_query("2")
