import * as d3 from 'd3';

export const createSemiPie = d3.pie().startAngle(-Math.PI / 2).endAngle(Math.PI / 2).sort(null);
export const createPie = d3.pie().sort(null);
export const createArc = (innerRadius, outerRadius) => (
  d3.arc().innerRadius(innerRadius).outerRadius(outerRadius)
);
