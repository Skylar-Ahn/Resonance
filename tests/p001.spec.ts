import { test, expect, type Page } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const concert = '/demo/concerts/concert-demo-001';
const seat = `${concert}/seat`;
const original = '연주자의 움직임을 가까이 보고 싶다';
const balanced = '전체 음향 균형 우선';

async function screenshot(page: Page, device: string, name: string) {
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(img => img.decode().catch(() => undefined))); });
  const directory = path.join('docs', 'tasks', 'P-001-captures');
  await mkdir(directory, { recursive: true });
  await page.screenshot({ path: path.join(directory, `${device}-${name}.png`), fullPage: true, animations: 'disabled' });
}
async function noOverflow(page: Page) {
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
}

test('App Home -> For You -> Overview -> Seat, all recommendations stay synchronized', async ({ page }, info) => {
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/demo');
  await expect(page.getByText('온보딩 완료', { exact: true })).toBeVisible();
  await expect(page.getByRole('navigation', { name: '주 메뉴' }).locator('[aria-current]')).toHaveCount(0);
  await expect(page.getByAltText('노란 resonance 레이블의 검은 LP, 기본 정지 상태')).toBeVisible();
  expect(await page.locator('img').evaluate(img => (img as HTMLImageElement).naturalWidth)).toBeGreaterThan(0);
  await noOverflow(page);
  await screenshot(page, info.project.name, 'home');
  await page.getByRole('link', { name: 'For You 둘러보기' }).click();
  await expect(page).toHaveURL(/\/demo\/for-you$/);
  await noOverflow(page);
  await screenshot(page, info.project.name, 'for-you');
  await page.getByRole('link', { name: '데모 실내악 공연', exact: true }).click();
  await expect(page.getByRole('heading', { name: '데모 실내악 공연', exact: true })).toBeVisible();
  await noOverflow(page);
  await screenshot(page, info.project.name, 'overview');
  await page.getByRole('link', { name: 'Seat', exact: true }).click();
  await expect(page.getByTestId('option-close').filter({ visible: true })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-highlighted=true]').filter({ visible: true })).toHaveCount(1);
  await page.getByRole('button', { name: '앙상블 균형 추천안' }).click();
  await expect(page.getByTestId('selected-seat-label').filter({ visible: true })).toHaveText('1층 B구역 7열 11~14번');
  expect(await page.locator('[data-highlighted=true]').filter({ visible: true }).evaluateAll(nodes => nodes.map(node => node.getAttribute('data-seat-id')))).toEqual(['B-7-11', 'B-7-12', 'B-7-13', 'B-7-14']);
  await expect(page.getByTestId('selected-reason').filter({ visible: true })).toContainText('전체적인 균형');
  await noOverflow(page);
  await screenshot(page, info.project.name, 'seat');
  await page.getByRole('link', { name: 'Overview', exact: true }).click();
  await page.getByRole('link', { name: 'Seat', exact: true }).click();
  await expect(page.getByTestId('option-balance').filter({ visible: true })).toHaveAttribute('aria-pressed', 'true');
  expect(errors).toEqual([]);
});

test('Current Need applies, cancels, survives navigation, resets without changing Concert Taste', async ({ page }, info) => {
  await page.goto(seat);
  await page.getByRole('button', { name: '추천 기준 조정', exact: true }).click();
  await page.getByLabel('이번 공연의 관람 기준').fill(balanced);
  await expect(page.getByTestId('taste-original').filter({ visible: true })).toHaveText(original);
  await screenshot(page, info.project.name, 'current-need');
  await page.getByRole('button', { name: '이번 추천에 적용' }).click();
  await expect(page.getByTestId('current-need').filter({ visible: true })).toHaveText(balanced);
  await expect(page.getByTestId('option-balance').filter({ visible: true })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByTestId('selected-reason').filter({ visible: true })).toContainText('미리 작성된 모의 응답');
  await page.getByRole('button', { name: '추천 기준 조정', exact: true }).click();
  await page.getByLabel('이번 공연의 관람 기준').fill('취소할 입력');
  await page.getByRole('button', { name: '취소', exact: true }).click();
  await expect(page.getByTestId('current-need').filter({ visible: true })).toHaveText(balanced);
  await page.getByRole('button', { name: '유틸리티 메뉴' }).click();
  await page.getByRole('link', { name: /My Concert Taste/ }).click();
  await expect(page.getByTestId('profile-experience').filter({ visible: true })).toHaveText(original);
  await page.goBack();
  await expect(page.getByTestId('current-need').filter({ visible: true })).toHaveText(balanced);
  await page.getByRole('button', { name: 'Current Need 초기화' }).click();
  await expect(page.getByTestId('option-close').filter({ visible: true })).toHaveAttribute('aria-pressed', 'true');
  await page.getByRole('button', { name: '추천 기준 조정', exact: true }).click();
  await expect(page.getByTestId('taste-original').filter({ visible: true })).toHaveText(original);
  await expect(page.getByLabel('이번 공연의 관람 기준')).toHaveValue('');
});

test('all mock states recover and partial data is explicit', async ({ page }) => {
  for (const route of ['/demo/for-you', seat]) {
    await page.goto(`${route}?scenario=loading`);
    await expect(page.getByRole('heading', { name: '모의 추천을 준비하고 있어요.' })).toBeVisible();
    await expect(page.getByRole('heading', { name: '모의 추천을 준비하고 있어요.' })).not.toBeVisible();
    for (const scenario of ['empty', 'error', 'unsupported']) {
      await page.goto(`${route}?scenario=${scenario}`);
      await expect(page.getByText('DEMO SCENARIO')).toBeVisible();
      await page.getByRole('button', { name: scenario === 'error' ? '다시 시도' : '기본 데모로 돌아가기' }).click();
      await expect(page).toHaveURL(new RegExp(`${route}$`));
      await expect(page.getByText('DEMO SCENARIO')).not.toBeVisible();
    }
  }
  await page.goto(`${seat}?scenario=partial`);
  await expect(page.getByRole('status')).toContainText('일부 정보 없음');
  await page.goto(`${concert}?scenario=partial`);
  await expect(page.getByText('정보 미제공', { exact: true })).toBeVisible();
});

test('three options, alternate concerts, direct entry, reload and unknown paths', async ({ page }) => {
  await page.goto(`${seat}?scenario=three`);
  await expect(page.getByRole('button', { name: /추천안$/ })).toHaveCount(3);
  await page.getByRole('button', { name: '무대의 대화 추천안' }).click();
  await expect(page.getByTestId('selected-seat-label').filter({ visible: true })).toHaveText('1층 A구역 5열 9~10번');
  await expect(page.locator('[data-highlighted=true]').filter({ visible: true })).toHaveCount(2);
  await page.reload();
  await expect(page.getByTestId('option-close').filter({ visible: true })).toHaveAttribute('aria-pressed', 'true');
  await page.goto('/demo/concerts/concert-demo-002/seat');
  await expect(page.getByRole('heading', { name: '데모 피아노 리사이틀' })).toBeVisible();
  await page.goto('/demo/for-you');
  await page.getByRole('link', { name: /좌석 추천 · 모의/ }).first().click();
  await expect(page).toHaveURL(new RegExp(`${seat}$`));
  await page.goto('/demo/concerts/not-a-concert');
  await expect(page.getByRole('heading', { name: '공연을 찾을 수 없어요.' })).toBeVisible();
});

test('bookmarks and utilities remain visible with explicit scope boundaries', async ({ page }) => {
  await page.goto(concert);
  await page.getByRole('button', { name: '데모 실내악 공연 북마크 · 이번 데모 범위 밖' }).click();
  await expect(page.getByRole('dialog')).toContainText('실제 처리는 실행되지 않습니다');
  await page.getByRole('button', { name: '확인', exact: true }).click();
  await page.getByRole('button', { name: '유틸리티 메뉴' }).click();
  for (const label of ['Account', 'My Concert Taste', 'Bookmarks', 'Settings']) await expect(page.getByRole('dialog').getByRole('link', { name: new RegExp(label) })).toBeVisible();
  await page.getByRole('link', { name: /Bookmarks/ }).click();
  await expect(page.getByRole('tab', { name: 'Concerts' })).toHaveAttribute('aria-selected', 'true');
  await page.getByRole('tab', { name: 'Articles' }).click();
  await expect(page.getByRole('tabpanel', { name: 'Articles' })).toContainText('아티클 북마크');
  await expect(page.getByRole('heading', { name: '이번 데모 범위 밖입니다.' })).toBeVisible();
  await noOverflow(page);
});

test('keyboard selection, dialog focus, map zoom and no external services', async ({ page }) => {
  const external: string[] = [];
  page.on('request', request => { if (!request.url().startsWith('http://127.0.0.1:3000') && !request.url().startsWith('data:')) external.push(request.url()); });
  await page.goto(seat);
  await expect(page.locator('[data-demo-ready]')).toHaveAttribute('data-demo-ready', 'true');
  await page.getByTestId('option-balance').filter({ visible: true }).focus();
  await page.keyboard.press('Enter');
  await expect(page.getByTestId('option-balance').filter({ visible: true })).toHaveAttribute('aria-pressed', 'true');
  await page.getByRole('button', { name: '추천 기준 조정', exact: true }).click();
  await expect(page.getByLabel('이번 공연의 관람 기준')).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page.getByRole('button', { name: '추천 기준 조정', exact: true })).toBeFocused();
  await page.getByLabel('좌석도 확대').selectOption('2');
  await noOverflow(page);
  // The scrollable map has a keyboard focus target even when no seat is for sale.
  await page.locator('[aria-label="좌석 배치도 스크롤 영역"]').filter({ visible: true }).focus();
  await expect(page.locator('[aria-label="좌석 배치도 스크롤 영역"]').filter({ visible: true })).toBeFocused();
  expect(external).toEqual([]);
});

test('selected recommendation and need persist across all viewport sizes', async ({ page }) => {
  await page.goto(seat);
  await page.getByRole('button', { name: '추천 기준 조정', exact: true }).click();
  await page.getByLabel('이번 공연의 관람 기준').fill(balanced);
  await page.getByRole('button', { name: '이번 추천에 적용' }).click();
  await page.getByText('데모 상태 확인', { exact: true }).click();
  await page.getByLabel('모의 응답 상태').selectOption('error');
  await page.getByRole('button', { name: '다시 시도' }).click();
  for (const size of [{ width: 390, height: 844 }, { width: 820, height: 1180 }, { width: 1440, height: 900 }]) {
    await page.setViewportSize(size);
    await noOverflow(page);
    await expect(page.getByTestId('current-need').filter({ visible: true })).toHaveText(balanced);
    await expect(page.getByTestId('selected-seat-label').filter({ visible: true })).toHaveText('1층 B구역 7열 11~14번');
    await expect(page.locator('[data-highlighted=true]').filter({ visible: true })).toHaveCount(4);
  }
});
