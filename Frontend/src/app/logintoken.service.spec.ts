import { TestBed } from '@angular/core/testing';

import { LogintokenService } from './logintoken.service';

describe('LogintokenService', () => {
  let service: LogintokenService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LogintokenService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
