package cern.accsoft.steering.jmad.modeldefs.defs;

import static org.junit.Assert.assertNotNull;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized.Parameters;

import cern.accsoft.steering.jmad.domain.ex.JMadModelException;
import cern.accsoft.steering.jmad.domain.optics.Optic;
import cern.accsoft.steering.jmad.model.JMadModel;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinition;
import cern.accsoft.steering.jmad.service.JMadService;
import cern.accsoft.steering.jmad.service.JMadServiceFactory;

/**
 * This is a JUnit4 test case, that loops through all available models and checks several simple conditions.
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
@RunWith(value = org.junit.runners.Parameterized.class)
public class AllModelsTest {

    private static final Logger LOGGER = Logger.getLogger(AllModelsTest.class);

    /** The model definition to test */
    private final JMadModelDefinition modelDefinition;

    @BeforeClass
    public static void initLog4J() {
        BasicConfigurator.configure();
        Logger.getRootLogger().setLevel(Level.INFO);
    }

    @AfterClass
    public static void resetLog4J() {
        BasicConfigurator.resetConfiguration();
    }

    /** The service to get all the definitions and to create the models */
    private static final JMadService JMAD_SERVICE = JMadServiceFactory.createJMadService();

    /**
     * The constructor: It takes one parameter
     * 
     * @param modelDefinition The model definition to test
     */
    public AllModelsTest(String modelDefinitionName, JMadModelDefinition modelDefinition) {
        this.modelDefinition = modelDefinition;
    }

    /**
     * provides the parameters for the tests
     * 
     * @return all model definitions as parameters for JUnit
     */
    @Parameters
    public static final Collection<Object> getModelDefinitions() {
        List<Object> parameterArrays = new ArrayList<Object>();
        for (JMadModelDefinition definition : JMAD_SERVICE.getModelDefinitionManager().getAllModelDefinitions()) {
            parameterArrays.add(new Object[] { definition.getName(), definition });
        }
        return parameterArrays;
    }

    /*
     * Test methods
     */

    /**
     * Simply tests if opening the model is possible. Then it closes it again
     * 
     * @throws JMadModelException if the model-creation fails
     */
    @Test
    public void testOpenModel() throws JMadModelException {
        LOGGER.info("");
        LOGGER.info("==== [START] Testing model '" + this.modelDefinition + "'. ====");
        assertNotNull("Model definition must not be null", this.modelDefinition);

        /* create the model */
        JMadModel model = JMAD_SERVICE.createModel(modelDefinition);
        assertNotNull("The created model must not be null.", model);
        LOGGER.info("Model '" + model + "' successfully created.");

        /* init the model */
        model.init();
        LOGGER.info("Model '" + model + "' successfully initialized.");

        /* test all optics definitions and recalculation of the optic */
        for (OpticsDefinition opticsDefinition : this.modelDefinition.getOpticsDefinitions()) {
            model.setActiveOpticsDefinition(opticsDefinition);
            Optic optic = model.getOptics();
            assertNotNull("Optic must not be null", optic);
            LOGGER.info("Optics values for optic '" + opticsDefinition + "' successfully retrieved.");
        }

        /* and close it again */
        model.cleanup();
        LOGGER.info("Model '" + model + "' successfully cleaned.");

        /* and remove it from the manager */
        JMAD_SERVICE.getModelManager().removeModel(model);
        LOGGER.info("==== [FINISHED] Testing model '" + this.modelDefinition + "'. ====");
        LOGGER.info("");
    }
}
