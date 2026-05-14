import { TestBed } from '@angular/core/testing';

import { Standing } from './standing';

describe('Standing', () => {
  let service: Standing;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Standing);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
