import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';

/*--------------ICONS------------------
  https://fontawesome.com/v5/cheatsheet 
  -------------------------------------
*/

import { 
    faPlay, 
    faCompress,
    faCamera,
    faPieChart,
    faPowerOff,
    faExpand,
    faCircleXmark,
    faCircleExclamation,
    faCircleInfo,
    faArrowDown,
} from '@fortawesome/free-solid-svg-icons';

library.add(
    faPlay,
    faCompress,
    faCamera,
    faPieChart,
    faPowerOff,
    faExpand,
    faCircleXmark,
    faCircleExclamation,
    faCircleInfo,
    faArrowDown
);

export default {
    'Play': <FontAwesomeIcon icon={faPlay} />,
    'Compress': <FontAwesomeIcon icon={faCompress} />,
    'Camera': <FontAwesomeIcon icon={faCamera} />,
    'PieChart': <FontAwesomeIcon icon={faPieChart} />,
    'Power': <FontAwesomeIcon icon={faPowerOff} />,
    'Expand': <FontAwesomeIcon icon={faExpand} />,
    'Info': <FontAwesomeIcon icon={faCircleInfo} />,
    'Warning': <FontAwesomeIcon icon={faCircleExclamation} />,
    'Error': <FontAwesomeIcon icon={faCircleXmark} />,
    'ArrowDown': <FontAwesomeIcon icon={faArrowDown} />,
};