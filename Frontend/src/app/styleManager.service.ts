import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StyleManagerService {
  private blurBackground = new BehaviorSubject<boolean>(false);

  blurState$ = this.blurBackground.asObservable();

  constructor() { }

  setBlurBackground(value: boolean) {
    this.blurBackground.next(value);
  }
}
