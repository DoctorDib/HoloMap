import { FormFieldTypeEnums } from '../Common/enumerations';

export default [
    { // Section
        title: 'Example Section title',
        rows: [
            [ // row
                [ // column
                    { type: FormFieldTypeEnums.Extra, index: 0 }, 
                    { type: FormFieldTypeEnums.Extra, index: 1, name: 'test' }, 
                ],
                [ // column
                    { type: FormFieldTypeEnums.Extra, index: 0 },
                ],
                [ // column
                    { type: FormFieldTypeEnums.TextInput, name: 'Text name', key: 'test-key', placeholder: 'Enter Text Name...' },
                    { type: FormFieldTypeEnums.TextInput, name: 'Second name', key: 'second-test', placeholder: 'Enter Second Name...' },
                ],
                [ // column
                    { type: FormFieldTypeEnums.TextInput, name: 'Another text', key: 'test-key' },
                ],
            ],
        ],
    },
    { // Section
        title: 'Second Section',
        rows: [
            [ // row
                [ // column
                    { type: FormFieldTypeEnums.Extra, index: 0 }, 
                    { type: FormFieldTypeEnums.Extra, index: 1, name: 'test' }, 
                ],
                [ // column
                    { type: FormFieldTypeEnums.Extra, index: 0 },
                ],
                [ // column
                    { type: FormFieldTypeEnums.TextInput, name: 'Text name', key: 'test-key', placeholder: 'Enter Text Name...' },
                    { type: FormFieldTypeEnums.TextInput, name: 'Second name', key: 'second-test', placeholder: 'Enter Second Name...' },
                ],
                [ // column
                    { type: FormFieldTypeEnums.TextInput, name: 'Another text', key: 'test-key' },
                ],
            ],
        ],
    },
];