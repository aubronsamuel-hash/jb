export default function autoprefixer() {
  return {
    postcssPlugin: 'autoprefixer-stub',
    Once() {
      /* noop */
    }
  };
}

autoprefixer.postcss = true;
