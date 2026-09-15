'use client';
import { createContext, useContext, useEffect, useReducer, useState, type Dispatch } from 'react';
import { demoReducer, initialState, type DemoAction, type DemoState } from '@/lib/demo';

const Context = createContext<{ state: DemoState; dispatch: Dispatch<DemoAction> } | null>(null);
export function DemoProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(demoReducer, initialState);
  const [ready, setReady] = useState(false);
  useEffect(() => setReady(true), []);
  return <Context.Provider value={{ state, dispatch }}><div data-demo-ready={ready} inert={!ready}>{children}</div></Context.Provider>;
}
export function useDemo() {
  const context = useContext(Context);
  if (!context) throw new Error('DemoProvider is required');
  return context;
}
