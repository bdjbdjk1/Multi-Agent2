import React from 'react';
import { Row, Col } from 'antd';
import { getChildrenToRender } from './utils';

class Content7 extends React.Component {
    getBlockChildren = (data) =>
        data.map(($item) => {
            const { title, img, content, ...rest } = $item;
            return (
                <li key={rest.name} {...rest}>
                    <span {...img}>
                        <img src={img.children} width="100%" alt="img" />
                    </span>
                    <h2 {...title}>{title.children}</h2>
                    <div {...content}>{content.children}</div>
                </li>
            );
        });

    render() {
        const { dataSource, ...props } = this.props;

        return (
            <div {...props} {...dataSource.wrapper}>
                <Row {...dataSource.OverPack}>
                    <Col {...dataSource.textWrapper}>
                        <div {...dataSource.titleWrapper}>
                            {dataSource.titleWrapper.children.map(getChildrenToRender)}
                        </div>
                        <ul {...dataSource.block}>
                        </ul>
                    </Col>
                    <Col {...dataSource.img}>
                        <img src={dataSource.img.children} width="100%" alt="img" />
                    </Col>
                </Row>
            </div>
        );
    }
}

export default Content7;
