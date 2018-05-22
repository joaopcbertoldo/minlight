import argparse


# valid max function maker
def valid_max(name, dtype, max):
    err_msg_template = f"Not a valid {name} max: " + '{s}'
    err_msg_template += f"{name} max must be a {dtype} less than or equal to {max}."

    # define the function to be returned
    def fun(s):

        # format the error message template
        err_msg = err_msg_template.format(s=s)

        try:
            arg = dtype(s)

            if not arg <= max:
                # raise a arparser's exception
                raise argparse.ArgumentTypeError(err_msg)

            return arg

        except Exception:
            # raise a arparser's exception
            raise argparse.ArgumentTypeError(err_msg)

    return fun


# valid min function maker
def valid_min(name, dtype, min):
    err_msg_template = f"Not a valid {name} min: " + '{s}'
    err_msg_template += f"{name} min must be a {dtype} greater than or equal to {min}."

    # define the function to be returned
    def fun(s):

        # format the error message template
        err_msg = err_msg_template.format(s=s)

        try:
            arg = dtype(s)

            if not arg >= min:
                # raise a arparser's exception
                raise argparse.ArgumentTypeError(err_msg)

            return arg

        except Exception:
            # raise a arparser's exception
            raise argparse.ArgumentTypeError(err_msg)

    return fun


# valid n for discretisation function maker
def valid_n_discretisation(name, min):
    err_msg_template = f"Not a valid number of {name} to test: " + '{s}'
    err_msg_template += f"It must be an int greater than or equal to {min}."

    def fun(s: str):

        # format the error message template
        err_msg = err_msg_template.format(s=s)

        try:
            # conversion
            i = int(s)

            # check limits
            if not i >= min:

                # raise a arparser's exception
                raise argparse.ArgumentTypeError(err_msg)

            return i

        except Exception:
            # raise a arparser's exception
            raise argparse.ArgumentTypeError(err_msg)

    return fun


# valid borned integer
def valid_borned_int(name, min, max):
    err_msg_template = f"Not a valid {name}: " + '{s}. '
    err_msg_template += f"It must be an int between '{min}' and '{max}'."

    def fun(s: str):

        # format the error message template
        err_msg = err_msg_template.format(s=s)

        try:
            # conversion
            i = int(s)

            # check limits
            if not i >= min or not i <= max:
                # raise a arparser's exception
                raise argparse.ArgumentTypeError(err_msg)

            return i

        except Exception:
            # raise a arparser's exception
            raise argparse.ArgumentTypeError(err_msg)

    return fun


# valid borned float
def valid_borned_float(name, min, max):
    err_msg_template = f"Not a valid {name}: " + '{s}. '
    err_msg_template += f"It must be an float between '{min}' and '{max}'."

    def fun(s: str) -> float:

        # format the error message template
        err_msg = err_msg_template.format(s=s)

        try:
            # conversion
            i = float(s)

            # check limits
            if not i >= min or not i <= max:
                # raise a arparser's exception
                raise argparse.ArgumentTypeError(err_msg)

            return i

        except Exception:
            # raise a arparser's exception
            raise argparse.ArgumentTypeError(err_msg)

    return fun


def valid_alias(s: str):

