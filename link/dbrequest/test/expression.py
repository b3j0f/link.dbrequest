# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from unittest import main

from link.dbrequest.expression import E, F
from link.dbrequest.comparison import C


class ExpressionTest(UTCase):
    def test_simple_expr(self):
        e = E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'ref',
                'val': 'propname'
            }
        )

    def test_expr_math(self):
        e = E('propname') * 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            [
                {
                    'name': 'ref',
                    'val': 'propname'
                },
                {
                    'name': 'op',
                    'val': '*'
                },
                {
                    'name': 'val',
                    'val': 5
                }
            ]
        )

    def test_expr_func(self):
        e = F('funcname', E('propname'), E('propname') * 5)
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'func',
                'val': {
                    'func': 'funcname',
                    'args': [
                        {
                            'name': 'ref',
                            'val': 'propname'
                        },
                        [
                            {
                                'name': 'ref',
                                'val': 'propname'
                            },
                            {
                                'name': 'op',
                                'val': '*'
                            },
                            {
                                'name': 'val',
                                'val': 5
                            }
                        ]
                    ]
                }
            }
        )

    def test_in_condition(self):
        c = C('prop1') == E('prop2')
        ast = c.get_ast()

        self.assertEqual(
            ast,
            [
                {
                    'name': 'prop',
                    'val': 'prop1'
                },
                {
                    'name': 'cond',
                    'val': '=='
                },
                {
                    'name': 'ref',
                    'val': 'prop2'
                }
            ]
        )

        c = C('prop1') == (E('prop2') + E('prop3'))
        ast = c.get_ast()

        self.assertEqual(
            ast,
            [
                {
                    'name': 'prop',
                    'val': 'prop1'
                },
                {
                    'name': 'cond',
                    'val': '=='
                },
                [
                    {
                        'name': 'ref',
                        'val': 'prop2'
                    },
                    {
                        'name': 'op',
                        'val': '+'
                    },
                    {
                        'name': 'ref',
                        'val': 'prop3'
                    }
                ]
            ]
        )


if __name__ == '__main__':
    main()