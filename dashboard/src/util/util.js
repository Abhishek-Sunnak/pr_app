export const createHash = (array, key) => {
  const hash = {};
  array.forEach((item) => {
    hash[item[key]] = item;
  });
  return hash;
};