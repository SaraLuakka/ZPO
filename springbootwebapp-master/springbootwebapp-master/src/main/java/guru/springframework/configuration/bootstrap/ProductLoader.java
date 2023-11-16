package guru.springframework.configuration.bootstrap;

import guru.springframework.domain.Product;
import guru.springframework.repositories.ProductRepository;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationListener;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;

@Component
public class ProductLoader implements ApplicationListener<ContextRefreshedEvent> {

    private ProductRepository productRepository;

    private Logger log = LogManager.getLogger(ProductLoader.class);

    @Autowired
    public void setProductRepository(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {

        Product shirt = new Product();
        shirt.setDescription("ABC");
        shirt.setPrice(new BigDecimal("3"));
        shirt.setImageUrl("https://giphy.com/gifs/brownsugarapp-ugh-stressed-stressing-7MDZS8zS1ixtJAUEul");
        shirt.setProductId("123");
        productRepository.save(shirt);

        log.info("ABC - id: " + shirt.getId());

        Product mug = new Product();
        mug.setDescription("QWERTY");
        mug.setImageUrl("https://giphy.com/gifs/brownsugarapp-ugh-stressed-stressing-7MDZS8zS1ixtJAUEul");
        mug.setProductId("000");
        mug.setPrice(new BigDecimal("5"));
        productRepository.save(mug);

        log.info("QWERTY - id:" + mug.getId());
    }
}
