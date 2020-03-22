
class GitParser:

    @staticmethod
    def parser_status(status: str):
        if line.startswith('On branch'):
            return 'branch', line.replace('On branch ', '')
        elif 'new file' in line:
            return 'new', line.replace('\tnew file:', '').strip()
        elif 'modified' in line:
            return 'modified', line.replace('\tmodified:', '').strip()
        elif 'renamed' in line:
            return 'modified', line.replace('\trenamed:', '').strip()
        elif line.startswith('\t'):
            return 'untracked', line.strip()