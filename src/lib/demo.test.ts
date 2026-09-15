import { describe, expect, it } from 'vitest';
import { demoReducer, demoUser, initialState, recommendations, seats } from './demo';

describe('P-001 fixture integrity', () => {
  it('resolves every recommended individual seat and range to unique map coordinates', () => {
    const ids = new Set(seats.map(seat => seat.id));
    expect(ids.size).toBe(256);
    for (const option of recommendations('', true)) {
      expect(option.seatIds.every(id => ids.has(id))).toBe(true);
      expect(new Set(option.seatIds).size).toBe(option.seatIds.length);
    }
    expect(recommendations()[1].seatIds).toEqual(['B-7-11', 'B-7-12', 'B-7-13', 'B-7-14']);
  });
  it('supports two and three options without mutating the default mock result', () => {
    expect(recommendations()).toHaveLength(2);
    expect(recommendations('', true)).toHaveLength(3);
    expect(recommendations('전체 음향 균형 우선')[0].id).toBe('balance');
    expect(recommendations()[0].id).toBe('close');
    expect(recommendations()[1].reason).not.toContain('이번 Current Need');
  });
  it('preserves arbitrary input without claiming a semantic recommendation', () => {
    const state = demoReducer(initialState, { type: 'apply', concertId: 'one', need: '  아주 조용한 자리  ' });
    expect(state.byConcert.one.need).toBe('아주 조용한 자리');
    expect(state.byConcert.one.selected).toBe('close');
  });
});

describe('Current Need isolation', () => {
  it('applies, selects and clears without changing long-term Concert Taste', () => {
    const original = JSON.stringify(demoUser);
    const applied = demoReducer(initialState, { type: 'apply', concertId: 'one', need: '전체 음향 균형 우선' });
    const selected = demoReducer(applied, { type: 'select', concertId: 'one', selected: 'close' });
    const cleared = demoReducer(selected, { type: 'clear', concertId: 'one' });
    for (const state of [applied, selected, cleared]) {
      expect(state.user).toBe(demoUser);
      expect(JSON.stringify(state.user)).toBe(original);
    }
    expect(initialState.byConcert).toEqual({});
    expect(cleared.byConcert.one.need).toBe('');
  });
  it('separates drafts and committed needs across concerts', () => {
    const applied = demoReducer(initialState, { type: 'apply', concertId: 'one', need: '전체 음향 균형 우선' });
    const draft = demoReducer(applied, { type: 'draft', concertId: 'two', draft: '다른 기준' });
    expect(draft.byConcert.one.need).toBe('전체 음향 균형 우선');
    expect(draft.byConcert.two.need).toBe('');
    expect(draft.byConcert.two.draft).toBe('다른 기준');
  });
  it('resets demo state and keeps onboarding complete', () => {
    const applied = demoReducer(initialState, { type: 'apply', concertId: 'one', need: '전체 음향 균형 우선' });
    const reset = demoReducer(applied, { type: 'reset' });
    expect(reset.byConcert).toEqual({});
    expect(reset.user.onboardingCompleted).toBe(true);
    expect(reset.user.concertTaste.content).toBeTruthy();
  });
});
