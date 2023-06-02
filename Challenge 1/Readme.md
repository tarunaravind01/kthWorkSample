# Ansible CLI app

This is a cli tool written in python that uses Ansible to configure online instances. It accepts instance names as input on the command line and leverages Ansible to perform the actual configuration tasks. The configuration process includes compiling and installing a "hello world" C program on the target instances.

Basic working of the application:

1. The user provides one or more instance names as input when running the CLI app.
2. The Python CLI app executes an Ansible playbook, passing the instance names as variables to the playbook.
3. The Ansible playbook uses an external Ansible role to compile and install the "hello world" C program on the target instances.
4. The playbook interacts with the target instances via SSH, utilizing the information provided in the Ansible inventory file.
5. The Ansible role creates a temporary directory on each target instance using the **`ansible.builtin.file`** module, compiles the C program using the **`ansible.builtin.command`** module, and copies the compiled binary to the desired location on the target instances.
6. The Ansible playbook completes the execution, and the Python CLI app displays a success message to indicate that the configuration is completed for each specified instance.

By leveraging this CLI tool, users can easily configure multiple online instances by simply providing the instance names as input, automating the compilation and installation of a C program on those instances using Ansible, and ensuring a smooth and consistent configuration process.

To run the application,

```bash
python cliApp.py <instance names>

or

python3 cliApp.py <instance names>
```

We can also easily add testing for this tool,

For example this is a python test written for this application that ensures that wrong instance names are handled well and also that the app run properly,

```python
import unittest
from subprocess import run, PIPE

class AppTestCase(unittest.TestCase):
    def test_app_runs_without_errors(self):
        # Test case to ensure the app runs without any errors
        result = run(['python3', 'cliApp.py', 'instance1'], stdout=PIPE, stderr=PIPE, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("instance1", result.stdout)
        self.assertIn("Configuration completed successfully", result.stdout)

    def test_app_handles_invalid_instance_name(self):
        # Test case to ensure the app handles invalid instance name gracefully
        result = run(['python3', 'cliApp.py', 'invalid_instance'], stdout=PIPE, stderr=PIPE, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Could not match supplied host pattern", result.stderr)

if __name__ == '__main__':
    unittest.main()
```

A model/example test to test the ansible role is as follows,

```yaml
#this is a rough example, might not work with the tool

---
- name: Test Ansible Role
  hosts: localhost
  tasks:
    - name: Include the configure.yml playbook
      include_playbook: configure.yml
      vars:
        target: "mock_instance"

    - name: Check if hello program is compiled
      stat:
        path: /usr/local/bin/hello
      register: hello_program

    - name: Assert that hello program exists
      assert:
        that:
          - hello_program.stat.exists
        fail_msg: "Hello program does not exist in /usr/local/bin"
```

In this example, we create a test playbook (**`test.yml`**) that includes the **`configure.yml`** playbook. We target the **`localhost`** as the host since it's a mock instance for testing purposes.

After running the **`configure.yml`** playbook, we use the **`stat`** module to check if the **`hello`** program is compiled and available in the **`/usr/local/bin`** directory. Finally, we use the **`assert`** module to ensure that the **`hello`** program exists. If the assertion fails, it displays a failure message.

To run the Ansible role tests, execute the test playbook (**`test.yml`**) using the **`ansible-playbook`** command, passing the test inventory file (**`test_inventory.ini`**) and the test playbook as arguments.

The main purpose of these tests here are to show that these can be written for more complex applications where tests are needed to make sure that the functionality does not break after each and every integration.
