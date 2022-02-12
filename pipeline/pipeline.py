import datetime

import luigi

from .tasks.build_fct import BuildFct

today = datetime.date.today().isoformat()

class Pipeline(luigi.WrapperTask):
    def requires(self):
        yield BuildFct(today=today)
