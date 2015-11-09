from os import path, makedirs


def folder_construct(template_name):
        local_path = path.dirname(path.abspath(__file__))
        template_dir = path.join(local_path, "output\\" + template_name)
        outjif = path.join(template_dir, "jif_output")
        feed_d = path.join(template_dir, "feed_data")
        exit_d = path.join(template_dir, "exit_data")

        if not path.exists(template_dir):
            makedirs(template_dir)
            makedirs(outjif)
            makedirs(feed_d)
            makedirs(exit_d)

        return [outjif, feed_d, exit_d]
