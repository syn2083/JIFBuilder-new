from random import choice, randint
from os import path
from jiftemplater import Template
from prog_utilities import folder_construct

__author__ = 'venom'

"""This module handles establishing the class to record a JIF template. The class creates an object which will
attach to a database, through SQLAlchemy. Along with the database record set, it has builtin assemblers for the
job ticket and piece manifesting, where appropriate."""


class JIFBuilder(Template):
    def piece_builder(self, piece_id):
        plist = []
        bstr = "\n"
        sheet_count = None

        plist.append("   <Piece>")
        plist.append("    <ID>{pieceid}</ID>".format(pieceid=str(piece_id).zfill(6)))

        if not int(self.var_sheets):
            sheet_count = 2
            plist.append("    <TotalSheets>2</TotalSheets>")
        else:
            sheet_count = randint(1, 15)
            plist.append("    <TotalSheets>{totals}</TotalSheets>".format(totals=str(sheet_count)))
        plist.append("   </Piece>")

        return [bstr.join(plist), sheet_count]

    def gen_jifs(self):
        jtype = []
        acct = []
        jname = []
        bstr = "\n"

        out_jif = folder_construct(self.template_name)[0]

        self.current_jobid = self.id_to_int()

        for i in self.job_type.split(','):
            jtype.append(i.strip())
        for i in self.account.split(','):
            acct.append(i.strip())
        for i in self.job_name.split(','):
            jname.append(i.strip())

        for i in range(0, self.num_jifs):
            jif_strings = []
            sheet_list = []
            jif_strings.append("""<?xml version="1.0" encoding="UTF-8"?>\n <JobTicket>\n <Version>2.2</Version>""")
            jif_strings.append(" <JobID>{jobid}</JobID>".format(jobid=self.id_to_str(self.current_jobid)))
            jif_strings.append(" <JobType>{jobtype}</JobType>".format(jobtype=choice(jtype)))
            jif_strings.append(" <JobName>{jobname}</JobName>".format(jobname=choice(jname)))
            jif_strings.append(" <AccountID>{accountid}</AccountID>".format(accountid=choice(acct)))
            jif_strings.append(" <StartSequence>000001</StartSequence>")
            jif_strings.append(" <EndSequence>{lastnumber}</EndSequence>".format(lastnumber=str(self.num_pieces)
                                                                                 .zfill(6)))
            jif_strings.append(" <PieceCount>{piececount}</PieceCount>".format(piececount=str(self.num_pieces)))
            jif_strings.append(" <CreationDate>{creation}</CreationDate>".format(creation=self.creation))
            jif_strings.append(" <JobDeadLine>{deadline}</JobDeadLine>".format(deadline=self.deadline))
            jif_strings.append(" <PrintMode>1</PrintMode>\n <PageComposition>2</PageComposition>")
            jif_strings.append(" <ProcessingPhases>{pphase}</ProcessingPhases>".format(pphase=self.proc_phase))
            jif_strings.append(" <EndProcess>{endproc}</EndProcess>".format(endproc=self.end_phase))
            jif_strings.append(" <ProductionLocation>{prodloc}</ProductionLocation>".format(prodloc=self.prod_loc))
            if self.piece_level == 1:
                jif_strings.append("  <JobManifest>")
                for t in range(1, (int(self.num_pieces)) + 1):
                    result = self.piece_builder(t)
                    jif_strings.append(result[0])
                    sheet_list.append(result[1])
                jif_strings.append("  </JobManifest>")
            jif_strings.append(" </JobTicket>\n")
            jstr = bstr.join(jif_strings)
            filename = path.join(out_jif, self.id_to_str(self.current_jobid) + ".jif")
            with open(filename, 'w') as fp:
                fp.write(jstr)
            fp.close()
            if self.feed_data is 1:
                self.gen_feed_data(sheet_list)
            if self.exit_data is 1:
                self.gen_exit_data()
            self.current_jobid += 1

    def gen_feed_data(self, num_sheets=None):
        out_str = "\n"
        out_path = folder_construct(self.template_name)[1]
        sheet_strings = []
        job_string = str(self.current_jobid).zfill(len(self.job_id))

        for i in range(1, self.num_pieces + 1):
            for t in range(1, num_sheets[i - 1] + 1):
                sheet_strings.append("{jobid}{pieceid}{cur_sheet}{total_sheet}".format(jobid=job_string,
                                                                                       pieceid=str(i).zfill(6),
                                                                                       cur_sheet=str(t).zfill(2),
                                                                                       total_sheet=str
                                                                                       (num_sheets[i - 1]).zfill(2)))
        filename = path.join(out_path, "feed_" + job_string + ".txt")
        with open(filename, 'w') as fp:
            fp.write(out_str.join(sheet_strings))
        fp.close()

    def gen_exit_data(self):
        out_str = "\n"
        out_path = folder_construct(self.template_name)[2]
        piece_strings = []
        job_string = str(self.current_jobid).zfill((len(self.job_id)))

        for i in range(1, self.num_pieces + 1):
            piece_strings.append("{jobid}{pieceid}".format(jobid=job_string, pieceid=str(i).zfill(6)))

        filename = path.join(out_path, "exit_" + job_string + ".txt")
        with open(filename, 'w') as fp:
            fp.write(out_str.join(piece_strings))
        fp.close()

    def __repr__(self):
        return "<BaseJIF(template_name='%s', piece_level='%s', num_jifs='%s')>" % \
               (self.template_name, self.piece_level, self.num_jifs)

