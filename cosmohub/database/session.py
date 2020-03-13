# -*- coding: utf-8 -*-
import contextlib
import logging


log = logging.getLogger(__name__)

# https://gist.github.com/obeattie/210032
@contextlib.contextmanager
def transactional_session(session, read_only=False):
    """\
    Context manager which provides transaction management for the nested block.
    A transaction is started when the block is entered, and then either
    committed if the block exits without incident, or rolled back if an error is
    raised.
    """
    try:
        if read_only:
            session.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ ONLY DEFERRABLE")
        yield session
        session.flush()

    except BaseException:
        # Roll back if the nested block raised an error
        session.rollback()
        raise

    else:
        session.commit()

    finally:
        session.close()
