import implbpvappcontext


def entry_point():

    ctx = implbpvappcontext.ImplBPVAppContext("RESP_metadata.csv", "RESP_TXR")
    ctx.run_app()


if __name__ == '__main__':
    entry_point()
