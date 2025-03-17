/* eslint no-undef: 0 */
/* eslint arrow-parens: 0 */
import React from 'react';
import { enquireScreen } from 'enquire-js';
import Banner5 from './Banner5';
import Feature40 from './Feature4';
import Feature10 from './Feature1';
import Feature20 from './Feature2';

import {
    Banner50DataSource,
    Feature40DataSource,
    Feature10DataSource,
    Feature20DataSource
} from './data.source';
import './less/antMotionStyle.less';

let isMobile;
enquireScreen((b) => {
    isMobile = b;
});

export default class HomeTemplate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isMobile,
            pages: [
                <Banner5 key="Banner5_0" id="Banner5_0" dataSource={Banner50DataSource} isMobile={isMobile} />,
                <Feature40 key="Feature40_1" id="Feature40_1" dataSource={Feature40DataSource} isMobile={isMobile} />,
                <Feature10 key="Feature10_2" id="Feature10_2" dataSource={Feature10DataSource} isMobile={isMobile} />,
                <Feature20 key="Feature20_3" id="Feature20_3" dataSource={Feature20DataSource} isMobile={isMobile} />
            ],
        };
    }

    componentDidMount() {
        // 适配手机屏幕
        enquireScreen((b) => {
            this.setState({ isMobile: !!b });
        });
    }

    render() {
        const { pages } = this.state;

        return (
            <div
                className="templates-wrapper"
                ref={(d) => {
                    this.dom = d;
                }}
            >
                {pages}
            </div>
        );
    }
}
