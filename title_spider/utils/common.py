import time

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

class UrlGenerator(object):

    def __init__(self, url_pattern, max_depth, entity_path):
        self.url_pattern = url_pattern
        self.max_depth = max_depth
        self.entity_path = entity_path

    def __iter__(self):
        with open(self.entity_path) as f:
            for line in f:
                line = line.strip()
                for i in range(self.max_depth):
                    yield line, self.url_pattern % (line, i)

class UrlGenerator2(object):

    def __init__(self, url_pattern, entity_path):
        self.url_pattern = url_pattern
        self.entity_path = entity_path

    def __iter__(self):
        with open(self.entity_path) as f:
            for line in f:
                line = line.strip()
                yield line, self.url_pattern % line


class UrlGenerator3(object):

    def __init__(self, url, entity_path):
        self.url = url
        self.entity_path = entity_path

    def __iter__(self):
        with open(self.entity_path) as f:
            for line in f:
                line = line.strip()
                yield line, self.url


class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)