import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalwithshopComponent } from './modalwithshop.component';

describe('ModalwithshopComponent', () => {
  let component: ModalwithshopComponent;
  let fixture: ComponentFixture<ModalwithshopComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalwithshopComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalwithshopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
