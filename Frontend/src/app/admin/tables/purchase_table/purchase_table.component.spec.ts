import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Purchase_tableComponent } from './purchase_table.component';

describe('PurchaseTableComponent', () => {
  let component: Purchase_tableComponent;
  let fixture: ComponentFixture<Purchase_tableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Purchase_tableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Purchase_tableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
