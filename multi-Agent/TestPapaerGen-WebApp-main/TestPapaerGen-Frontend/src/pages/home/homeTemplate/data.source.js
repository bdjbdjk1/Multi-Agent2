import React from 'react';
import homeImage from '../../../../public/img/home.png';
import home2Image from '../../../../public/img/home2.png';
import rot from'../../../../public//CarbonMachineLearning.png'
import pdf from'../../../../public//IcRoundFolderOpen.png'
import code from'../../../../public//MaterialSymbolsCodeBlocksOutlineSharp.png'
export const Banner50DataSource = {
  wrapper: { className: 'home-page-wrapper banner5' },
  page: { className: 'home-page banner5-page' },
  childWrapper: {
    className: 'banner5-title-wrapper',
    children: [
      {
        name: 'title',
        children: (
            <span>
            <p>Eclipse Exam</p>
            <p>智能、精准、高效</p>
          </span>
        ),
        className: 'banner5-title',
      },
      {
        name: 'content',
        className: 'banner5-content',
        children: (
            <span>
            <p>上传知识内容，多智能体即可自动出题，可选择不同题型、难度。既可手动组卷，也可自动组卷，还支持导出功能。</p>
          </span>
        ),
      },
      {
        name: 'button',
        className: 'banner5-button-wrapper',
        children: {
          href: '#/login',
          className: 'banner5-button',
          type: 'primary',
          children: '开始使用',
        },
      },
    ],
  },
  image: {
    className: 'banner5-image',
    children: homeImage,
  },
};
export const Feature40DataSource = {
  wrapper: { className: 'home-page-wrapper content6-wrapper' },
  OverPack: { className: 'home-page content6' },
  textWrapper: { className: 'content6-text', xs: 24, md: 20 },
  titleWrapper: {
    className: 'title-wrapper',
    children: [
      {
        name: 'title',
        children: 'Eclipse Exam提供的功能',
        className: 'title-h1',
      },
      {
        name: 'content',
        className: 'title-content',
        children: '基于大语言模型的高效试题生成与组卷系统',
      },
    ],
  },

  block: {
    children: [
      {
        name: 'block0',
        img: {
          children:rot,
          className: 'content6-icon',
        },
        title: { className: 'content6-title', children: '智能' },
        content: {
          className: 'content6-content',
          children:
              '去除繁琐的人工出题过程，多智能体运用，显著提升出题效率',
        },
      },
      {
        name: 'block1',
        img: {
          className: 'content6-icon',
          children:pdf,
        },
        title: { className: 'content6-title', children: '个性' },
        content: {
          className: 'content6-content',
          children:
              '精准和个性化试题需求，简单导入文件即可快速生成题目，支持选择、判断、填空、多种题型。',
        },
      },
      {
        name: 'block2',
        img: {
          className: 'content6-icon',
          children:code,
        },
        title: { className: 'content6-title', children: '算法' },
        content: {
          className: 'content6-content',
          children:
              '贪心算法与遗传算法组卷，精准组合生成完整试卷，确保试卷的科学性与合理性',
        },
      },
    ],
  },
};
export const Feature10DataSource = {
  wrapper: { className: 'home-page-wrapper content1-wrapper' },
  OverPack: { className: 'home-page content1' },
  titleWrapper: {
    className: 'title-wrapper',
    children: [
      {
        name: 'title',
        children: '多智能体框架结构图',
        className: 'title-h1',
      },
    ],
  },
  img: {
    children: home2Image,
    className: 'content1-img',
    xs: 40,
    md: 24,
  },
};
export const Feature20DataSource = {
  wrapper: { className: 'home-page-wrapper content-wrapper' },
  OverPack: { className: 'home-page content2', playScale: 0.3 },
  textWrapper: { className: 'content2-text', md: 54, xs: 24 },
  title: { className: 'content2-title', children: '让出题更高效，让组卷更合理',style: { textAlign: 'center' } },
  content: {
    className: 'content2-content',
    children:
        '推动智能与传统教育的集合，通过智能体协作提高试题生成效率，减少出题时间，同时确保试题的完整性和合理性。',
    style: { textAlign: 'center' }
  },
};
export const Footer01DataSource = {
  wrapper: { className: 'home-page-wrapper footer0-wrapper' },
  OverPack: { className: 'home-page footer0', playScale: 0.05 },
  copyright: {
    className: 'copyright',
    children: (
        <span>
        ©2018 <a href="https://motion.ant.design">Ant Motion</a> All Rights
        Reserved
      </span>
    ),
  },
};