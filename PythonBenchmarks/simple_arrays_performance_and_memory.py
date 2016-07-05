"""
Created on Sep 18, 2015

@author: Vadym Yusanenko
"""

from sys import getsizeof
from timeit import Timer


OUTPUT_LEFT_JUSTIFICATION = 25


def print_inspection_title(title, is_first_title=False):
    """ Prints inspection title in a properly formatted way. """
    print '%s=====\n%s\n=====' % ('\n\n' if not is_first_title else '', title)


def inspect_container_size(object_type, size=1000):
    """ Prints amount of memory required to represent specifiied object. """

    if object_type == TYPE_LIST:
        container = [item for item in xrange(size)]
    elif object_type == TYPE_SET:
        container = ({item for item in xrange(size)})
    elif object_type == TYPE_TUPLE:
        container = tuple(item for item in xrange(size))
    else:
        raise Exception('This object is not supported.')

    print 'Type: %sSize: %s' % (
        type(container).__name__.ljust(OUTPUT_LEFT_JUSTIFICATION),
        getsizeof(container)
    )


def run_timing_test(
    container_type, statement, setup_instruction='pass', number=1000000
):
    """ Prints properly formatted timing report for specified statement. """
    print 'Type: %sTime: %s' % (
        container_type.ljust(OUTPUT_LEFT_JUSTIFICATION),
        Timer(setup=setup_instruction, stmt=statement).timeit(number)
    )


def generate_container_declaration(
    object_type, size=1000, variable_name='container'
):
    """
    Generate container declaration string suitable in use with timeit utility.
    """

    if object_type in (
        TYPE_LIST, TYPE_TUPLE, TYPE_SET
    ):
        return '%s = %s( [ item for item in xrange(%s) ] )' % (
            variable_name, object_type.__name__, size
        )
    else:
        raise Exception('This object is not supported.')


def inspect_container_iteration(object_type, size=100):
    """ Test iteration over container. """
    # Adding marker to identify which exact check do we perform at this moment.
    object_type_name = object_type.__name__
    run_timing_test(
        object_type_name,
        'for item in container: pass',
        generate_container_declaration(object_type, size)
    )


def inspect_container_addition(object_type, statements=10):
    """
    Test addition of new elements to containers.
    "statements" value represents amount of additions.
    """

    if object_type == TYPE_LIST:
        statement_template = 'container.append(%s)'
    elif object_type == TYPE_SET:
        statement_template = 'container.add(%s)'
    elif object_type == TYPE_TUPLE:
        statement_template = 'container+=(%s,)'
    else:
        raise Exception('This object is not supported.')

    if object_type in (
        TYPE_LIST, TYPE_TUPLE, TYPE_SET
    ):
        statement = ';'.join(
            [statement_template % item for item in xrange(statements)]
        )
    else:
        raise Exception('This object is not supported.')

    run_timing_test(
        object_type.__name__,
        statement,
        generate_container_declaration(object_type, 0),
        10000
    )


def inspect_container_membership(object_type, size=1000):
    """
    Test speed of membership detection in container.
    """

    run_timing_test(
        object_type.__name__,
        'item in container;',
        generate_container_declaration(object_type, size)
    )


def inspect_container_concatenation(object_type, size=100):
    """
    Test speed concatenating two containers of the same type.
    """

    if object_type == TYPE_SET:
        concatenation_statement = 'container=container.union(container_2)'
    elif object_type in (TYPE_LIST, TYPE_TUPLE):
        concatenation_statement = 'container += container_2'
    else:
        raise Exception('Unsupported object type')

    run_timing_test(
        object_type.__name__,
        concatenation_statement,
        '%s; %s' % (
            generate_container_declaration(object_type, size),
            generate_container_declaration(object_type, size, 'container_2')
        ),
        10000
    )


def container_removal_by_index(object_type, size=10000):
    """
    Test speed of removal element by index.
    """

    object_type_name = object_type.__name__

    if object_type == TYPE_LIST:
        removal_statement_template = 'del container[%s]'
    elif object_type in (TYPE_SET, TYPE_TUPLE):
        removal_statement_template = (
            'container=%s'
            '(item[1] for item in enumerate(container) if item[0]!=%s)'
            %
            (object_type_name, '%s')
        )
    else:
        raise Exception('Unsupported object type')

    removal_statement = ';'.join(
        tuple(
            removal_statement_template % item_count
            for item_count in reversed(xrange(size))
        )
    )

    run_timing_test(
        object_type_name,
        removal_statement,
        generate_container_declaration(object_type, size),
        1
    )


def container_removal_by_value(object_type, size=10000):
    """
    Test speed of removal element by value.
    IMPORTANT NOTE: list supports removal of all similar values or only the
                    first occurence.
    """

    object_type_name = object_type.__name__

    if object_type in (TYPE_LIST, TYPE_TUPLE):
        removal_statement_template_all = (
            (
                'container=%s'
                '(item[1] for item in enumerate(container) if item[0]!=%s)'
            ) % (object_type_name, '%s')
        )
        if object_type == TYPE_LIST:
            removal_statement_template_list = 'container.remove(%s)'
    elif object_type == TYPE_SET:
        removal_statement_template_all = 'container.remove(%s)'
    else:
        raise Exception('Unsupported object type')

    removal_statement_all = ';'.join(
        tuple(
            removal_statement_template_all % item_count
            for item_count in reversed(xrange(size))
        )
    )

    run_timing_test(
        object_type_name,
        removal_statement_all,
        generate_container_declaration(object_type, size),
        1
    )

    if object_type == TYPE_LIST:
        removal_statement_first = ';'.join(
            tuple(
                removal_statement_template_list % item_count
                for item_count in reversed(xrange(size))
            )
        )
        run_timing_test(
            object_type_name + ' [first occurence]',
            removal_statement_first,
            generate_container_declaration(object_type, size),
            1
        )


TYPE_LIST = type(list())
TYPE_SET = type(set())
TYPE_TUPLE = type(tuple())


print_inspection_title('Memory', True)
inspect_container_size(TYPE_LIST)
inspect_container_size(TYPE_SET)
inspect_container_size(TYPE_TUPLE)

print_inspection_title('Iteration')
inspect_container_iteration(TYPE_LIST)
inspect_container_iteration(TYPE_SET)
inspect_container_iteration(TYPE_TUPLE)

print_inspection_title('Addition')
inspect_container_addition(TYPE_LIST)
inspect_container_addition(TYPE_SET)
inspect_container_addition(TYPE_TUPLE)

print_inspection_title('Membership')
inspect_container_membership(TYPE_LIST)
inspect_container_membership(TYPE_SET)
inspect_container_membership(TYPE_TUPLE)

print_inspection_title('Concatenation')
inspect_container_concatenation(TYPE_LIST)
inspect_container_concatenation(TYPE_SET)
inspect_container_concatenation(TYPE_TUPLE)

print_inspection_title('Removal by index')
container_removal_by_index(TYPE_LIST)
container_removal_by_index(TYPE_SET)
container_removal_by_index(TYPE_TUPLE)

print_inspection_title('Removal by value')
container_removal_by_value(TYPE_LIST)
container_removal_by_value(TYPE_SET)
container_removal_by_value(TYPE_TUPLE)
