'use client';
import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import s from './demo.module.css';

export function Dialog({ open, onClose, title, children }: { open: boolean; onClose: () => void; title: string; children: React.ReactNode }) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = ref.current;
    if (open && !dialog?.open) {
      dialog?.showModal();
      dialog?.querySelector<HTMLElement>('textarea')?.focus();
    }
    else if (!open && dialog?.open) dialog.close();
  }, [open]);
  return <dialog ref={ref} className={s.dialog} aria-label={title} onCancel={onClose} onClose={onClose} onClick={event => { if (event.target === event.currentTarget) onClose(); }}>
    {open && <><div className={s.dialogHeading}><h2>{title}</h2><button type="button" className={s.iconButton} onClick={onClose} aria-label="닫기" title="닫기"><X size={21} /></button></div>
    {children}</>}
  </dialog>;
}
