import { faChevronRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import classNames from "classnames";
import React from "react";

import { Card } from "components/ui/Card";

import { ConnectionBlockItem, Content } from "./components/ConnectionBlockItem";
import styles from "./ConnectionBlock.module.scss";

interface IProps {
  itemFrom?: { name: string; icon?: string };
  itemTo?: { name: string; icon?: string };
}

const ConnectionBlock: React.FC<IProps> = (props) => (
  <Card className={classNames(styles.lightContentCard)}>
    {props.itemFrom ? <ConnectionBlockItem {...props.itemFrom} /> : <Content className={styles.extraBlock} />}
    <FontAwesomeIcon className={styles.arrow} icon={faChevronRight} />
    {props.itemTo ? <ConnectionBlockItem {...props.itemTo} /> : <Content className={styles.extraBlock} />}
  </Card>
);

export default ConnectionBlock;
