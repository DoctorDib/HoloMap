import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// eslint-disable-next-line import/no-extraneous-dependencies
import { library } from '@fortawesome/fontawesome-svg-core';

/*--------------ICONS------------------
  https://fontawesome.com/v5/cheatsheet 
  -------------------------------------
*/

import { 
    faPlay, 
    faCompress
} from '@fortawesome/free-solid-svg-icons';

library.add(
    faPlay,
    faCompress
);

export default {
    'Play': <FontAwesomeIcon icon={faPlay} />,
    'Compress': <FontAwesomeIcon icon={faCompress} />,
};