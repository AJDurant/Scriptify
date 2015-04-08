from gluon.sqlhtml import OptionsWidget, add_class
from gluon.html import LABEL, INPUT, DIV

class BootstrapRadio(OptionsWidget):

    @classmethod
    def widget(cls, field, value, **attributes):
        """
        Generates a Bootstrap Radio Button
        """

        if isinstance(value, (list, tuple)):
            value = str(value[0])
        else:
            value = str(value)

        attr = cls._attributes(field, {}, **attributes)
        attr['_class'] = add_class(attr.get('_class'), 'web2py_radiowidget')

        requires = field.requires
        if not isinstance(requires, (list, tuple)):
            requires = [requires]
        if requires:
            if hasattr(requires[0], 'options'):
                options = requires[0].options()
            else:
                raise SyntaxError('widget cannot determine options of %s'
                                  % field)
        options = [(k, v) for k, v in options if str(v)]
        opts = []
        cols = attributes.get('cols', 1)
        totals = len(options)
        mods = totals % cols
        rows = totals / cols
        if mods:
            rows += 1

        for r_index in range(rows):
            tds = []
            for k, v in options[r_index * cols:(r_index + 1) * cols]:
                checked = {'_checked': 'checked'} if k == value else {}
                tds.append(
                    LABEL(
                        INPUT(
                            _type='radio',
                           _id='%s%s' % (field.name, k),
                           _name=field.name,
                           requires=attr.get('requires', None),
                           hideerror=True, _value=k,
                           value=value,
                           **checked),
                        v,
                        _for='%s%s' % (field.name, k)
                    )
                )
            opts.append(DIV(tds, _class='radio'))

        if opts:
            opts[-1][0][0]['hideerror'] = False
        return DIV(*opts, **attr)
