import { describe, it, expect } from 'vitest';
import { add } from '../src/math.js';

describe('math.add', () => {
    it('adds positive numbers', () => {
        expect(add(2, 3)).toBe(5);
    });
    it('adds negative numbers', () => {
        expect(add(-5, -7)).toBe(-12);
    });
    it('adds with string numbers', () => {
        expect(add('4', 6)).toBe(10);
    });
});
