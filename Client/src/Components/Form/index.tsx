// import React, { ReactElement, useEffect, useState } from 'react';
// import { useSelector } from 'react-redux';
// import classNames from 'classnames';

// import './form-style.scss';

// import InputField from '../Inputs/InputField';
// import Checkbox from '../Inputs/Checkbox';
// import DropDown from '../Inputs/DropDown';
// import { StateTypes } from '../../Interfaces/StateInterface';
// import { FormFieldTypeEnums } from '../../Common/enumerations';
// import { EncryptedValue } from '../../Common/Types';

// interface FormState {
//     Fields: Array<any>,
//     Extras?: Array<React.ReactElement>,
//     UpdateForm: (key: string, value: any)=>void,
//     FormData: Record<number | string, any>,
//     StartWithColumn?: boolean,
// }

// interface FieldInterface {
//     name: string,
//     rows: any,
//     key: string,
//     confidential: boolean,
//     type: number,
//     options: any,
//     placeholder: string,
//     index: number,
//     width?: string,
//     height?: string
// }

// const FormComponent = ({ Fields, Extras, UpdateForm, FormData, StartWithColumn = true }: FormState) : React.ReactElement => {
//     const [elements, setElements] = useState<Array<React.ReactElement>>([]);

//     const fieldTemplate = (field: FieldInterface, element: ReactElement, isRow: boolean): React.ReactElement => {
//         const axis: string = isRow ? 'row' : 'column';
//         return (
//             <div key={field.key} className={classNames(['form--element-container', `form--${axis}-element-container`])}
//                 style={{ width: field.width ?? '100%', height: field.height ?? '100%' }}
//             >
//                 <div className={classNames(['form--element', `form--${axis}-element`])}> 
//                     { field.name !== '' && <div className={'form--title'}> { field.name } </div> }
//                     <div className={'form--value'}> { element } </div>
//                 </div>
//             </div>
//         );
//     };
    
//     const getFieldElement = (field: FieldInterface): React.ReactElement => {
//         if (FormData === null) {
//             return;
//         }
        
//         // const shouldDisable: boolean = account !== undefined && FormData?.owner_id_aesn != undefined 
//         //     && account.id_aesn.EncryptedValue != (FormData?.owner_id_aesn as EncryptedValue)?.EncryptedValue;

//         const value: string = shouldDisable && field.confidential ? 'REDACTED' : FormData[field.key];

//         switch (field.type) {
//             case FormFieldTypeEnums.Extra:
//                 return fieldTemplate(field, Extras[field.index], false);
//             case FormFieldTypeEnums.TextInput:
//             case FormFieldTypeEnums.NumberInput:
//             case FormFieldTypeEnums.PasswordInput:
//                 return fieldTemplate(field, 
//                     <InputField ID={field.key}
//                         key={field.key}
//                         Disabled={shouldDisable}
//                         Type={
//                             field.type === FormFieldTypeEnums.TextInput
//                                 ? 'text'
//                                 : field.type === FormFieldTypeEnums.PasswordInput
//                                     ? 'password'
//                                     : 'number'
//                         }
//                         Value={value}
//                         OnChange={UpdateForm}
//                         Placeholder={field.placeholder}
//                     />,
//                     false,
//                 );
//             case FormFieldTypeEnums.Checkbox:
//                 return fieldTemplate(field, 
//                     <Checkbox ID={field.key} 
//                         key={field.key}
//                         Disabled={shouldDisable}
//                         Value={value !== undefined ? JSON.parse(value) : false}
//                         OnChange={UpdateForm} 
//                     />,
//                     false,
//                 );
//             case FormFieldTypeEnums.Splitter:
//                 return (
//                     <div key={field.key} className={'form-splitter'}>
//                         <div className={'form-splitter-line'}> </div>
//                         { field.name && <div className={'form-splitter-title'}> { field.name } </div> }
//                         <div className={'form-splitter-line'}> </div>
//                     </div>
//                 );
//             case FormFieldTypeEnums.Header:
//                 return (
//                     <div key={field.key} className={'form--header'}>
//                         { field.name && <div className={'form-splitter-title'}> { field.name } </div> }
//                     </div>
//                 );
//             case FormFieldTypeEnums.DropDown:
//                 return fieldTemplate(field,
//                     <DropDown Value={value} 
//                         key={field.key}
//                         Disabled={shouldDisable}
//                         ID={field.key} 
//                         OnChange={UpdateForm} 
//                         Options={field.options}/>,
//                     false,
//                 );
//         }

//         return <div> FIELD TYPE NOT FOUND </div>;
//     };

//     const generateRowOrColumn = (loopElement: Array<any>, layer: number, generateRow = true): React.ReactElement | Array<React.ReactElement> => 
//         loopElement.map((element, index) => Array.isArray(element) 
//             ? ( <div key={`el${index}`} className={classNames([
//                 layer <= 1 ? 'form--special-layer' : '',
//                 'form--container',
//                 `form--${generateRow ? 'row' : 'column'}-container`,
//             ])}>
//                 { generateRowOrColumn(element, layer++, !generateRow) }
//             </div> )
//             : getFieldElement(element));

//     const mapFields = (): void => {
//         const newElementsArr: Array<React.ReactElement> = [];
//         Fields.forEach(section => {
//             const newElements: React.ReactElement = generateRowOrColumn(section.rows, 0, StartWithColumn) as React.ReactElement;
//             newElementsArr.push(newElements);
//         });
//         setElements(newElementsArr);
//     };

//     useEffect(() => mapFields(), [Fields, FormData, Extras]);

//     return <div className={'form--fields-container'}> { elements } </div>;
// };

// export default FormComponent;