import { TestBed } from '@angular/core/testing';

import { Leader } from './leader';

describe('Leader', () => {
  let service: Leader;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Leader);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
