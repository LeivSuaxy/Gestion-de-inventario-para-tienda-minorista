import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  private booleanValue = new BehaviorSubject<boolean>(false);
  currentBooleanValue = this.booleanValue.asObservable();

  private triggerFunctionSource = new Subject<any>();
  triggerFunction$ = this.triggerFunctionSource.asObservable();

  constructor() { }

  changeBooleanValue(value: boolean) {
    this.booleanValue.next(value);
  }

  triggerFunction(functionName: string) {
    this.triggerFunctionSource.next(functionName);
  }
}
