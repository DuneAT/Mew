import unittest
from unittest.mock import patch, mock_open, MagicMock
import json

from utils.server_utils import (
    create_model_file,
    launch_ollama_server,
    request_answer_not_stream,
    request_answer_stream,
    request_answer,
    find_pid_by_port,
    kill_process,
    launch_backend_server
)


class TestServerUtils(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_create_model_file(self, mock_file):
        modelfile_text = "test content"
        create_model_file(modelfile_text)
        mock_file.assert_called_with("Modelfile", 'w')
        mock_file().write.assert_called_once_with(modelfile_text)

    @patch("os.system")
    def test_launch_ollama_server(self, mock_system):
        launch_ollama_server()
        mock_system.assert_called_with("ollama create mew_model -f Modelfile")

    @patch("requests.post")
    def test_request_answer_not_stream_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"response": "test response"})
        mock_post.return_value = mock_response

        response = request_answer_not_stream("test prompt")
        self.assertEqual(response, "test response")

    @patch("requests.post")
    def test_request_answer_not_stream_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        response = request_answer_not_stream("test prompt")
        self.assertEqual(response, "Server Error")

    @patch("requests.post")
    def test_request_answer_stream_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_lines = MagicMock(return_value=[json.dumps({"response": "chunk1"}).encode('utf-8'),
                                                           json.dumps({"response": "chunk2"}).encode('utf-8')])
        mock_post.return_value.__enter__.return_value = mock_response

        response = list(request_answer_stream("test prompt"))
        self.assertEqual(response, ["chunk1", "chunk2"])

    @patch("requests.post")
    def test_request_answer_stream_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value.__enter__.return_value = mock_response

        response = list(request_answer_stream("test prompt"))
        self.assertEqual(response, ["Server Error"])

    @patch("utils.server_utils.request_answer_not_stream")
    def test_request_answer_not_stream_mode(self, mock_request_answer_not_stream):
        mock_request_answer_not_stream.return_value = "test response"
        response = request_answer("test prompt")
        self.assertEqual(response, "test response")

    @patch("utils.server_utils.request_answer_stream")
    def test_request_answer_stream_mode(self, mock_request_answer_stream):
        mock_request_answer_stream.return_value = iter(["chunk1", "chunk2"])
        response = list(request_answer("test prompt"))
        self.assertEqual(response, ["chunk1", "chunk2"])

    @patch("subprocess.check_output")
    def test_find_pid_by_port_success(self, mock_check_output):
        mock_check_output.return_value = b"1234\n"
        pid = find_pid_by_port(11434)
        self.assertEqual(pid, 1234)

    @patch("subprocess.check_output")
    def test_find_pid_by_port_failure(self, mock_check_output):
        mock_check_output.side_effect = subprocess.CalledProcessError(
            1, 'lsof')
        pid = find_pid_by_port(11434)
        self.assertIsNone(pid)

    @patch("os.kill")
    def test_kill_process_success(self, mock_kill):
        kill_process(1234)
        mock_kill.assert_called_with(1234, signal.SIGTERM)

    @patch("os.kill")
    def test_kill_process_failure(self, mock_kill):
        mock_kill.side_effect = OSError("Error")
        with self.assertLogs(level='INFO') as log:
            kill_process(1234)
            self.assertIn(
                "Error terminating process 1234: Error", log.output[0])

    @patch("os.system")
    def test_launch_backend_server(self, mock_system):
        launch_backend_server()
        mock_system.assert_called_with("uvicorn main:app --reload")


if __name__ == '__main__':
    unittest.main()
