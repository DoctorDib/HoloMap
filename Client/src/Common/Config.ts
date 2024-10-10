import packageJson from '../../package.json';

export default {
    version: packageJson.version,

    cmd_console: {
        max_history: 5,
        interval_update: 5, //seconds
    },

    resolution: {
        width: packageJson.resolution.width,
        height: packageJson.resolution.height,
    },
};