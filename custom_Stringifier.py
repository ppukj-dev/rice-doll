import d20


booleanOps = ['=', '<', '<=', '>', '>=']


class BoolStringifier(d20.SimpleStringifier):
    """
    Transforms roll expressions into Markdown.
    """

    class _MDContext:
        def __init__(self):
            self.in_dropped = False

        def reset(self):
            self.in_dropped = False

    def __init__(self):
        super().__init__()
        self.target = 0
        self._context = self._MDContext()

    def stringify(self, the_roll):
        self._context.reset()
        return super().stringify(the_roll)

    def _stringify(self, node):
        if not node.kept and not self._context.in_dropped:
            self._context.in_dropped = True
            inside = super()._stringify(node)
            self._context.in_dropped = False
            return f"~~{inside}~~"
        return super()._stringify(node)

    def _str_expression(self, node):
        if(node.roll.op in booleanOps):
            self.target = node.roll.right.number
        return f"{self._stringify(node.roll.left)}"

    def _str_die(self, node):
        the_rolls = []
        for val in node.values:
            inside = self._stringify(val)
            if val.number == node.size:
                inside = f"**{inside}**"
            # elif val.number == 1 and self.target != 1: #might won't need this
            #    inside = f"**~~{inside}~~**"
            elif val.number < self.target:
                inside = f"~~{inside}~~"
            the_rolls.append(inside)
        return ', '.join(the_rolls)