from sqlalchemy import Column, Integer, String, VARCHAR
from database import Base


class Template(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True)
    template_name = Column(String)
    piece_level = Column(Integer)
    var_sheets = Column(Integer)
    total_sheets = Column(Integer)
    num_jifs = Column(Integer)
    job_id = Column(String)
    account = Column(String)
    job_name = Column(String)
    job_type = Column(String)
    num_pieces = Column(Integer)
    creation = Column(VARCHAR)
    deadline = Column(VARCHAR)
    proc_phase = Column(VARCHAR)
    end_phase = Column(Integer)
    prod_loc = Column(String)
    current_jobid = None
    feed_data = 0
    exit_data = 0

    def id_to_int(self):
        try:
            return int(self.job_id)
        except ValueError:
            return None

    def id_to_str(self, input_id):
        try:
            return str(input_id).zfill(len(self.job_id))
        except:
            return None
