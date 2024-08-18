import { QR } from "../Interfaces/StateInterface";

const QR_BLANK : QR = {
    detected_qrs: [],
};

const SETTINGS_BLANK : object = {
    def_pos_x: 0,
    def_pos_y: 0,
    def_size_width: 100,
    def_size_height: 100,
    drag_steps: 1,
    resize_steps: 1,
    time_interval_logger: 15,
    time_interval_ping: 15,
};

export { QR_BLANK, SETTINGS_BLANK, };