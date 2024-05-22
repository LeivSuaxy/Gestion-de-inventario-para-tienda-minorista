import { Injectable } from '@angular/core';

export interface Venta{
  id: number;
  imagen: string;
  titulo: string;
  precio: number;
  descripcion: string;
  cantidadStock: number;
}

@Injectable({
  providedIn: 'root'
})
export class CartService {
  cart: Venta[] = [];
  preciototal: number = 0;

  ventas: Venta[] = [
    {
      id: 1,
      imagen: '../../../../assets/img/Telefono.jpeg',
      titulo: 'S23 Ultra',
      precio: 1200,
      descripcion: 'Samsung Galaxy S23 Ultra, con 512GB de almacenamiento interno, 12GB de RAM, 5 camaras, 1 principal con' +
        '200MP, 1 gran angular de 50MP, 1 telefoto de 20MP, 1 macro de 5MP y 1 de profundidad de 2MP. Ademas de una pantalla' +
        'Super AMOLED.',
      cantidadStock: 270
    },
    {
      id: 2,
      imagen: '../../../../assets/img/Laptop.jpeg',
      titulo: 'Macbook',
      precio: 3400,
      descripcion: 'Una macbook mangrina',
      cantidadStock: 70
    },
    {
      id: 3,
      imagen: '../../../../assets/img/RAM.jpeg',
      titulo: 'RAM DDR5 16GB',
      precio: 5000,
      descripcion: 'Una RAM claramente hecha con IA',
      cantidadStock: 120
    },
    {
      id: 4,
      imagen: '../../../../assets/img/Carro.jpeg',
      titulo: 'Ferrari',
      precio: 5000000,
      descripcion: 'Un carro que nunca tendremos, pero ahi esta en una venta ficticia',
      cantidadStock: 20
    },
    {
      id: 5,
      imagen: '../../../../assets/img/Grafica.jpeg',
      titulo: 'NVIDIA RTX 7090',
      precio: 4000,
      descripcion: 'Una tarjeta grafica de NVIDIA que no se si sea asi porque bueno, tiene mas rgb que potencia',
      cantidadStock: 120
    },
    {
      id: 6,
      imagen: '../../../../assets/img/Raton.jpeg',
      titulo: 'Mouse GAMING 3000',
      precio: 150,
      descripcion: 'Erdiavlo pero que mouse papa que hacemos con esta vaina',
      cantidadStock: 200
    },
    {
      id: 7,
      imagen: '../../../../assets/img/RatonApple.jpeg',
      titulo: 'Mouse michi michi',
      precio: 5000,
      descripcion: 'Super caro, pero que mas da, total la gente de apple compra por comprar',
      cantidadStock: 100
    },
    {
      id: 8,
      imagen: '../../../../assets/img/Boligrafo.jpeg',
      titulo: 'Boligrafo',
      precio: 1,
      descripcion: 'La mejor oferta del mercado.',
      cantidadStock: 1000
    },
  ]

  addToCart(product: Venta) {
    if(!this.cart.includes(product)) this.cart.push(product);
    this.preciototal = 0;
    for (let i = 0; i < this.cart.length; i++) {
      this.preciototal += this.cart[i].precio;
    }
  }

  removeFromCart(productid: number) {
    this.cart = this.cart.filter(product => product.id !== productid);

    this.preciototal = 0;
    for (let i = 0; i < this.cart.length; i++) {
      this.preciototal += this.cart[i].precio;
    }
  }

  getCart() {
    return this.cart;
  }

  getPrecioTotal() {
    return this.preciototal;
  }

  isInCar(venta: Venta):boolean{
    return this.cart.includes(venta);
  }

  clearCart() {
    this.cart = [];
    return this.cart;
  }
}
