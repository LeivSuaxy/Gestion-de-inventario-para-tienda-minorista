import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StockcardsComponent } from './stockcards.component';

describe('StockcardsComponent', () => {
  let component: StockcardsComponent;
  let fixture: ComponentFixture<StockcardsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StockcardsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StockcardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
