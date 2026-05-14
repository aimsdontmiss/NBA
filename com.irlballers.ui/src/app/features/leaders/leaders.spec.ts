import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Leaders } from './leaders';

describe('Leaders', () => {
  let component: Leaders;
  let fixture: ComponentFixture<Leaders>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Leaders],
    }).compileComponents();

    fixture = TestBed.createComponent(Leaders);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
